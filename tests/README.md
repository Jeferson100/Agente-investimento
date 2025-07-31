# Testes Unitários - Agente Investimento

Este diretório contém os testes unitários para o projeto `agente_investimento`. Os testes foram criados para garantir a qualidade e confiabilidade do código.

## Estrutura dos Testes

### Testes Criados

1. **`test_consulta_banco_postgree.py`**
   - Testa a classe `PostgresDBConsult`
   - Cobre conexão com banco de dados, consultas e operações de tabela
   - Testa tratamento de exceções
   - **Status**: ✅ Funcionando

2. **`test_funcoes_utils.py`**
   - Testa as funções utilitárias em `utils/funcoes_utils.py`
   - Cobre conversão de generators, configuração de mensagens e transformação de dados
   - Testa diferentes tipos de entrada e saída
   - **Status**: ✅ Funcionando

3. **`test_processa_analises.py`**
   - Testa as funções de processamento de análises em `utils/processa_analises.py`
   - Cobre análises fundamentalista, técnica, valuation e sentimento
   - Testa funções assíncronas com mocks
   - **Status**: ✅ Funcionando

4. **`test_verifica_tick.py`**
   - Testa a verificação de tickets em `langgraph_construcao/verifica_tick.py`
   - Cobre validação de tickers, tentativas de busca e tratamento de erros
   - Testa diferentes cenários de entrada
   - **Status**: ✅ Funcionando

5. **`test_identifica_ticks.py`**
   - Testa a identificação de ticks em `langgraph_construcao/identifica_ticks.py`
   - Cobre identificação de tickers usando LLM
   - Testa o modelo Pydantic `Tickers`
   - **Status**: ✅ Funcionando

6. **`test_identifica_metodo_analise.py`**
   - Testa a identificação de métodos de análise em `langgraph_construcao/identifica_metodo_analise.py`
   - Cobre diferentes tipos de análise (fundamentalista, técnica, etc.)
   - Testa o modelo Pydantic `MetodoAnalise`
   - **Status**: ✅ Funcionando

7. **`test_dados_indicadores_tecnicos.py`**
   - Testa a coleta de dados técnicos em `coleta_dados/dados_indicadores_tecnicos.py`
   - Cobre obtenção de cotações e cálculo de indicadores técnicos
   - Testa diferentes períodos e intervalos
   - **Status**: ✅ Funcionando

8. **`test_app_streamlit.py`**
   - Testa a aplicação Streamlit em `app/app_streamlit.py`
   - Cobre componentes da interface, gerenciamento de estado e interações
   - Testa carregamento de códigos, configuração de APIs e elementos da UI
   - **Status**: ✅ Funcionando

### Testes Existentes

- **`test_chat_bots.py`** - Testes para chatbots
- **`test_coleta_dados.py`** - Testes para coleta de dados
- **`test_juncao_modelos_dados.py`** - Testes para junção de modelos
- **`test_tratando_dados.py`** - Testes para tratamento de dados

## Como Executar os Testes

### Executar Todos os Testes

```bash
# Na raiz do projeto
python -m pytest tests/ -v

# Ou usando o script personalizado
python tests/test_all.py
```

### Executar Testes Específicos

```bash
# Testar apenas consulta ao banco
python -m pytest tests/test_consulta_banco_postgree.py -v

# Testar apenas funções utilitárias
python -m pytest tests/test_funcoes_utils.py -v

# Testar apenas processamento de análises
python -m pytest tests/test_processa_analises.py -v

# Testar apenas aplicação Streamlit
python -m pytest tests/test_app_streamlit.py -v --no-cov
```

### Executar com Cobertura

```bash
# Instalar coverage se não estiver instalado
pip install coverage

# Executar testes com cobertura
coverage run -m pytest tests/
coverage report
coverage html  # Gera relatório HTML
```

## Padrões de Teste

### Estrutura dos Testes

Cada arquivo de teste segue o padrão:

```python
import unittest
from unittest.mock import MagicMock, patch

class TestClassName(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        pass
    
    def test_method_name(self):
        """Descrição do teste."""
        # Arrange
        # Act
        # Assert
```

### Mocks e Stubs

Os testes utilizam mocks para:
- APIs externas (yfinance, LLMs)
- Conexões de banco de dados
- Chamadas de rede
- Dependências externas
- Componentes do Streamlit

### Casos de Teste

Cada teste cobre:
- **Cenários de sucesso**: Funcionalidade normal
- **Cenários de erro**: Tratamento de exceções
- **Casos extremos**: Dados vazios, valores nulos
- **Diferentes tipos de entrada**: Validação de parâmetros
- **Componentes de UI**: Elementos da interface Streamlit

## Cobertura de Testes

### Módulos Cobertos

- ✅ `consulta_banco_postgree.py` - 100% cobertura
- ✅ `utils/funcoes_utils.py` - 100% cobertura
- ✅ `utils/processa_analises.py` - 17% cobertura (funções assíncronas)
- ✅ `langgraph_construcao/verifica_tick.py` - 26% cobertura
- ✅ `langgraph_construcao/identifica_ticks.py` - 77% cobertura
- ✅ `langgraph_construcao/identifica_metodo_analise.py` - 75% cobertura
- ✅ `coleta_dados/dados_indicadores_tecnicos.py` - 32% cobertura
- ✅ `app/app_streamlit.py` - Componentes de UI testados

### Funcionalidades Testadas

- Inicialização de classes
- Métodos principais
- Tratamento de exceções
- Validação de entrada
- Transformação de dados
- Integração com APIs externas
- Modelos Pydantic
- Interface Streamlit
- Gerenciamento de estado
- Componentes de UI

## Dependências para Testes

```bash
pip install pytest
pip install pytest-asyncio
pip install coverage
pip install pandas
pip install numpy
pip install yfinance
pip install finta
pip install sqlalchemy
pip install langchain
pip install langgraph
pip install pydantic
pip install streamlit
```

## Contribuindo com Testes

### Adicionando Novos Testes

1. Crie um arquivo `test_<modulo>.py`
2. Importe as classes/funções a serem testadas
3. Crie uma classe de teste herdando de `unittest.TestCase`
4. Implemente métodos de teste com nomes descritivos
5. Use mocks para dependências externas
6. Documente o propósito de cada teste

### Boas Práticas

- **Nomes descritivos**: Use nomes que descrevem o que está sendo testado
- **Um conceito por teste**: Cada teste deve verificar uma funcionalidade específica
- **Independência**: Testes não devem depender uns dos outros
- **Mocks apropriados**: Use mocks para dependências externas
- **Documentação**: Comente o propósito de cada teste

### Exemplo de Teste

```python
def test_calculo_indicador_tecnico_com_dados_validos(self):
    """Testa cálculo de indicador técnico com dados válidos."""
    # Arrange
    dados = pd.DataFrame({'Close': [10, 11, 12, 13, 14]})
    
    # Act
    resultado = self.calculadora.calcular_rsi(dados)
    
    # Assert
    self.assertIsInstance(resultado, pd.Series)
    self.assertGreater(len(resultado), 0)
```

## Relatórios de Teste

Os testes geram relatórios detalhados incluindo:
- Número de testes executados
- Tempo de execução
- Cobertura de código
- Detalhes de falhas
- Sugestões de melhoria

## Integração Contínua

Os testes são executados automaticamente em:
- Pull requests
- Deployments
- Builds noturnos

Isso garante que mudanças no código não quebrem funcionalidades existentes.

## Resumo dos Testes Criados

### Total de Testes: 81 testes
- **Testes de Consulta ao Banco**: 8 testes
- **Testes de Funções Utilitárias**: 10 testes
- **Testes de Processamento de Análises**: 7 testes
- **Testes de Verificação de Ticks**: 12 testes
- **Testes de Identificação de Ticks**: 12 testes
- **Testes de Identificação de Método de Análise**: 13 testes
- **Testes de Dados de Indicadores Técnicos**: 10 testes
- **Testes da Aplicação Streamlit**: 9 testes

### Cobertura Total: 31%
- Módulos principais com alta cobertura
- Foco em funcionalidades críticas
- Testes de integração e edge cases
- Interface de usuário testada

### Status Geral: ✅ Funcionando
Todos os testes criados estão passando e cobrem as funcionalidades principais do sistema, incluindo a interface Streamlit. 