#!/usr/bin/env python3
"""
Script para executar todos os testes unitários do projeto agente_investimento.
"""

import unittest
import sys
import os

# Adicionar o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar todos os testes
from tests.test_consulta_banco_postgree import TestPostgresDBConsult
from tests.test_funcoes_utils import TestFuncoesUtils
from tests.test_processa_analises import TestProcessaAnalises
from tests.test_verifica_tick import TestVerificaTick
from tests.test_identifica_ticks import TestIdentificaTicks
from tests.test_identifica_metodo_analise import TestIdentificaMetodoAnalise
from tests.test_dados_indicadores_tecnicos import TestDadosIndicadoresTecnicos



def run_all_tests():
    """Executa todos os testes unitários."""
    # Criar um test suite
    test_suite = unittest.TestSuite()
    
    # Adicionar todos os testes
    test_classes = [
        TestPostgresDBConsult,
        TestFuncoesUtils,
        TestProcessaAnalises,
        TestVerificaTick,
        TestIdentificaTicks,
        TestIdentificaMetodoAnalise,
        TestDadosIndicadoresTecnicos,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Executar os testes
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Retornar o código de saída
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    print("Executando todos os testes unitários...")
    print("=" * 50)
    
    exit_code = run_all_tests()
    
    print("=" * 50)
    if exit_code == 0:
        print("✅ Todos os testes passaram!")
    else:
        print("❌ Alguns testes falharam!")
    
    sys.exit(exit_code) 