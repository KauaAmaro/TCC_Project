#!/usr/bin/env python3

import requests
import json
import subprocess
import time
import os

def check_backend_running():
    print("=== VERIFICANDO BACKEND ===")
    try:
        response = requests.get("http://localhost:8000/", timeout=3)
        if response.status_code == 200:
            print("✅ Backend está rodando")
            return True
        else:
            print(f"⚠️ Backend respondeu com status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend não está rodando")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar backend: {e}")
        return False

def test_relatorio_endpoint():
    print("\n=== TESTANDO ENDPOINT /relatorio ===")
    try:
        response = requests.get("http://localhost:8000/relatorio", timeout=5)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dados recebidos: {len(data)} itens")
            
            if data:
                print("📋 Estrutura dos dados:")
                for i, item in enumerate(data[:3]):
                    print(f"   {i+1}. {json.dumps(item, ensure_ascii=False)}")
                return True
            else:
                print("⚠️ Array vazio retornado")
                return False
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"📄 Resposta: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def check_cors():
    print("\n=== VERIFICANDO CORS ===")
    try:
        response = requests.options("http://localhost:8000/relatorio", 
                                  headers={"Origin": "http://localhost:3000"})
        cors_headers = {
            "Access-Control-Allow-Origin": response.headers.get("Access-Control-Allow-Origin"),
            "Access-Control-Allow-Methods": response.headers.get("Access-Control-Allow-Methods"),
            "Access-Control-Allow-Headers": response.headers.get("Access-Control-Allow-Headers"),
        }
        print(f"📋 Headers CORS: {json.dumps(cors_headers, indent=2)}")
        
        if "http://localhost:3000" in str(cors_headers.get("Access-Control-Allow-Origin", "")):
            print("✅ CORS configurado corretamente")
            return True
        else:
            print("⚠️ CORS pode estar mal configurado")
            return False
    except Exception as e:
        print(f"❌ Erro ao verificar CORS: {e}")
        return False

def start_backend_if_needed():
    print("\n=== INICIANDO BACKEND SE NECESSÁRIO ===")
    if not check_backend_running():
        print("🚀 Tentando iniciar backend...")
        try:
            # Configurar PATH
            env = os.environ.copy()
            env['PATH'] = f"{os.path.expanduser('~')}/.local/bin:{env.get('PATH', '')}"
            
            # Iniciar backend em background
            process = subprocess.Popen([
                "python3", "backend/main.py"
            ], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Aguardar um pouco
            time.sleep(3)
            
            if check_backend_running():
                print("✅ Backend iniciado com sucesso!")
                return process
            else:
                print("❌ Falha ao iniciar backend")
                stdout, stderr = process.communicate(timeout=1)
                print(f"STDOUT: {stdout.decode()}")
                print(f"STDERR: {stderr.decode()}")
                return None
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return None
    else:
        return None

def main():
    print("🔧 DIAGNÓSTICO COMPLETO DO RELATÓRIO")
    print("=" * 50)
    
    # Verificar/iniciar backend
    backend_process = start_backend_if_needed()
    
    # Testes
    backend_ok = check_backend_running()
    endpoint_ok = test_relatorio_endpoint() if backend_ok else False
    cors_ok = check_cors() if backend_ok else False
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DO DIAGNÓSTICO:")
    print(f"   Backend rodando: {'✅' if backend_ok else '❌'}")
    print(f"   Endpoint /relatorio: {'✅' if endpoint_ok else '❌'}")
    print(f"   CORS configurado: {'✅' if cors_ok else '❌'}")
    
    if all([backend_ok, endpoint_ok, cors_ok]):
        print("\n🎉 TUDO OK! O relatório deve funcionar.")
        print("📱 Acesse: http://localhost:3000/relatorio")
    else:
        print("\n⚠️ PROBLEMAS ENCONTRADOS!")
        if not backend_ok:
            print("   - Inicie o backend: python3 backend/main.py")
        if not endpoint_ok:
            print("   - Verifique se há dados no banco")
        if not cors_ok:
            print("   - Verifique configuração CORS no backend")
    
    # Manter backend rodando se foi iniciado
    if backend_process:
        print(f"\n🔄 Backend rodando (PID: {backend_process.pid})")
        print("Pressione Ctrl+C para parar...")
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Parando backend...")
            backend_process.terminate()

if __name__ == "__main__":
    main()