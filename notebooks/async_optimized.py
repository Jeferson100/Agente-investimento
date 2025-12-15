"""
Versão otimizada das funções assíncronas para processamento de múltiplos tics.

Melhorias implementadas:
- Controle de concorrência com semáforo
- Retry automático com backoff exponencial
- Timeout para evitar travamentos
- Tratamento específico para rate limits
- Tracking de progresso em tempo real
- Estatísticas detalhadas ao final
"""

import time
import asyncio
from typing import Dict, List, Optional, Any
from asyncio import Semaphore, TimeoutError as AsyncTimeoutError

# ============================================================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================================================
MAX_CONCURRENT = 3  # Número máximo de requisições simultâneas (recomendado: 3-5)
MAX_RETRIES = 3  # Número máximo de tentativas em caso de erro
TIMEOUT_SECONDS = 300  # Timeout de 5 minutos por tic
RETRY_DELAY_BASE = 2  # Delay base para retry exponencial (segundos)

# ============================================================================
# FUNÇÃO OTIMIZADA PARA PROCESSAR UM TIC
# ============================================================================
async def _invoke_tic(
    tic: str, 
    data_inicio: str = "2023-01-01", 
    data_fim: str = "2025-01-01",
    retry_count: int = 0
) -> Optional[Dict[str, Any]]:
    """
    Processa um tic de forma assíncrona com retry automático e timeout.
    
    Melhorias implementadas:
    - Timeout para evitar travamentos
    - Retry automático com backoff exponencial
    - Tratamento específico para rate limits
    - Logging detalhado de progresso
    """
    try:
        start = time.time()
        logger.info(f"🚀 [{retry_count+1}/{MAX_RETRIES}] Iniciando {tic}")
        
        # Timeout para evitar travamentos indefinidos
        result = await asyncio.wait_for(
            graph_build.ainvoke(
                StateClassification({
                    "tic": tic,
                    "data_inicio": data_inicio,
                    "data_fim": data_fim,
                    "avaliacao_analise": "",
                    "description_avaliacao_analise": "",
                    "interacao": 0,
                })
            ),
            timeout=TIMEOUT_SECONDS
        )
        
        elapsed = time.time() - start
        logger.info(f"✅ {tic} concluído em {elapsed:.2f}s")
        return result
        
    except AsyncTimeoutError:
        logger.error(f"⏱️  Timeout ao processar {tic} após {TIMEOUT_SECONDS}s")
        return None
        
    except Exception as e:
        error_msg = str(e)
        logger.warning(f"⚠️  Erro ao processar {tic} (tentativa {retry_count+1}/{MAX_RETRIES}): {error_msg[:100]}")
        
        # Retry logic para rate limits e erros temporários
        if retry_count < MAX_RETRIES - 1:
            # Backoff exponencial com jitter aleatório
            delay = RETRY_DELAY_BASE ** (retry_count + 1) + (time.time() % 1)
            
            # Rate limit específico - esperar mais tempo
            if "rate limit" in error_msg.lower() or "429" in error_msg or "quota" in error_msg.lower():
                delay = min(delay * 3, 60)  # Máximo 60 segundos para rate limits
                logger.warning(f"🔄 Rate limit detectado para {tic}, aguardando {delay:.1f}s")
            else:
                logger.info(f"🔄 Aguardando {delay:.1f}s antes de retry para {tic}")
            
            await asyncio.sleep(delay)
            
            # Retry recursivo
            return await _invoke_tic(tic, data_inicio, data_fim, retry_count + 1)
        else:
            logger.error(f"❌ Falha definitiva ao processar {tic} após {MAX_RETRIES} tentativas")
            return None

# ============================================================================
# FUNÇÃO OTIMIZADA PARA PROCESSAR MÚLTIPLOS TICS
# ============================================================================
async def run_all_tics(
    tics: List[str], 
    data_inicio: str = "2023-01-01", 
    data_fim: str = "2025-01-01",
    max_concurrent: int = MAX_CONCURRENT
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Processa múltiplos tics em paralelo com controle de concorrência.
    
    Melhorias implementadas:
    - Controle de concorrência com semáforo
    - Tracking de progresso em tempo real
    - Estatísticas detalhadas ao final
    - Melhor tratamento de erros
    
    Args:
        tics: Lista de tickers para processar
        data_inicio: Data inicial
        data_fim: Data final
        max_concurrent: Número máximo de requisições simultâneas
        
    Returns:
        Dicionário com resultados por ticker
    """
    start_total = time.time()
    total_tics = len(tics)
    completed = 0
    failed = 0
    
    logger.info(f"📊 Iniciando processamento de {total_tics} tics com concorrência máxima de {max_concurrent}")
    
    # Semáforo para controlar concorrência e evitar sobrecarga
    semaphore = Semaphore(max_concurrent)
    
    async def bounded_invoke(tic: str) -> tuple[str, Optional[Dict[str, Any]]]:
        """Wrapper com controle de concorrência e tracking de progresso"""
        nonlocal completed, failed
        
        async with semaphore:
            result = await _invoke_tic(tic, data_inicio, data_fim)
            
            if result is None:
                failed += 1
            completed += 1
            
            # Log de progresso a cada 10% ou a cada tic se for menos de 10
            progress = (completed / total_tics) * 100
            if completed % max(1, total_tics // 10) == 0 or completed == total_tics:
                logger.info(
                    f"📈 Progresso: {completed}/{total_tics} ({progress:.1f}%) | "
                    f"Sucesso: {completed - failed} | Falhas: {failed}"
                )
            
            return (tic, result)
    
    # Criar todas as tasks
    tasks = [bounded_invoke(tic) for tic in tics]
    
    # Executar com gather (todas as tasks rodam em paralelo, respeitando o semáforo)
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Processar resultados
    results_dict = {}
    for item in results_list:
        if isinstance(item, Exception):
            logger.error(f"❌ Exceção não tratada: {item}")
            continue
        tic, result = item
        results_dict[tic] = result
    
    elapsed_total = time.time() - start_total
    success_count = completed - failed
    
    # Relatório final detalhado
    logger.info(
        f"\n{'='*60}\n"
        f"📊 RESUMO FINAL\n"
        f"{'='*60}\n"
        f"⏱️  Tempo total: {elapsed_total:.2f}s ({elapsed_total/60:.1f}min)\n"
        f"✅ Sucessos: {success_count}/{total_tics} ({(success_count/total_tics*100):.1f}%)\n"
        f"❌ Falhas: {failed}/{total_tics} ({(failed/total_tics*100):.1f}%)\n"
        f"⚡ Tempo médio por tic: {elapsed_total/total_tics:.2f}s\n"
        f"🚀 Throughput: {total_tics/(elapsed_total/60):.2f} tics/min\n"
        f"{'='*60}"
    )
    
    return results_dict

# ============================================================================
# EXEMPLO DE USO
# ============================================================================
# results = await run_all_tics(
#     tics=list_tics[:10],
#     data_inicio="2023-01-01",
#     data_fim="2025-01-01",
#     max_concurrent=MAX_CONCURRENT  # Ajuste conforme necessário (3-5 é recomendado)
# )

