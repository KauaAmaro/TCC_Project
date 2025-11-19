#!/usr/bin/env python3

import requests
import json

def test_relatorio_endpoint():
    print("=== TESTE DO ENDPOINT /relatorio ===")
    
    base_url = "http://localhost:8000"
    
    try:
        # Testar endpoint /relatorio
        print("🔗 Testando GET /relatorio...")
        response = requests.get(f"{base_url}/relatorio", timeout=5)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dados recebidos: {len(data)} itens")
            print(f"📄 Conteúdo: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # Validar estrutura
            if isinstance(data, list):
                print("✅ Formato de array correto")
                for i, item in enumerate(data):
                    if isinstance(item, dict) and 'descricao' in item and 'quantidade' in item:
                        print(f"✅ Item {i+1}: {item['descricao']} -> {item['quantidade']}")
                    else:
                        print(f"❌ Item {i+1} com estrutura inválida: {item}")
            else:
                print("❌ Resposta não é um array")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Backend não está rodando em http://localhost:8000")
        print("💡 Inicie o backend com: python3 backend/main.py")
    except requests.exceptions.Timeout:
        print("❌ Erro: Timeout na requisição")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_leituras_endpoint():
    print("\n=== TESTE DO ENDPOINT /leituras ===")
    
    base_url = "http://localhost:8000"
    
    try:
        response = requests.get(f"{base_url}/leituras", timeout=5)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Leituras encontradas: {len(data)}")
            
            if data:
                print("📋 Primeiras 3 leituras:")
                for i, item in enumerate(data[:3]):
                    print(f"   {i+1}. {item.get('codigo_barras')} - {item.get('descricao')} (qty: {item.get('quantidade')})")
            else:
                print("⚠️ Nenhuma leitura encontrada no banco")
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_relatorio_endpoint()
    test_leituras_endpoint()