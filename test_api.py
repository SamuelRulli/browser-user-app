#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando corretamente
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health Check OK")
            print(f"   Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Health Check falhou: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que está rodando.")
        return False
    except Exception as e:
        print(f"❌ Erro no Health Check: {e}")
        return False

def test_run_task_validation():
    """Testa validação do endpoint run-task"""
    print("\n🔍 Testando validação do endpoint run-task...")
    try:
        # Teste sem campo obrigatório
        response = requests.post(f"{BASE_URL}/api/v1/run-task", json={})
        if response.status_code == 400:
            print("✅ Validação funcionando corretamente")
            print(f"   Resposta: {response.json()}")
            return True
        else:
            print(f"❌ Validação não funcionou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no teste de validação: {e}")
        return False

def test_run_task_mock():
    """Testa o endpoint run-task com uma task simples (sem aguardar conclusão)"""
    print("\n🔍 Testando endpoint run-task (modo assíncrono)...")
    try:
        task_data = {
            "task": "Teste de API - apenas verificar se a requisição é processada",
            "wait_for_completion": False
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/run-task", json=task_data)
        print(f"   Status Code: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        
        if response.status_code == 200:
            result = response.json()
            if 'task_id' in result:
                print("✅ Task criada com sucesso")
                return result['task_id']
            else:
                print("❌ Resposta não contém task_id")
                return None
        else:
            print(f"❌ Falha ao criar task: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Erro ao testar run-task: {e}")
        return None

def test_get_task_status(task_id):
    """Testa o endpoint de status da task"""
    if not task_id:
        print("\n⏭️  Pulando teste de status (sem task_id)")
        return
        
    print(f"\n🔍 Testando endpoint de status para task {task_id}...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/task/{task_id}/status")
        print(f"   Status Code: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Status obtido com sucesso")
        else:
            print(f"❌ Falha ao obter status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro ao testar status: {e}")

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API Browser Use Wrapper\n")
    
    # Teste 1: Health Check
    if not test_health_check():
        print("\n❌ API não está respondendo. Verifique se está rodando em http://localhost:5000")
        return
    
    # Teste 2: Validação
    test_run_task_validation()
    
    # Teste 3: Run Task (assíncrono)
    task_id = test_run_task_mock()
    
    # Teste 4: Get Task Status
    test_get_task_status(task_id)
    
    print("\n🎉 Testes concluídos!")
    print("\n📝 Próximos passos:")
    print("   1. Importe a coleção postman_collection.json no Postman")
    print("   2. Configure sua BROWSER_USE_API_KEY")
    print("   3. Teste com tasks reais usando o Postman")

if __name__ == "__main__":
    main()
