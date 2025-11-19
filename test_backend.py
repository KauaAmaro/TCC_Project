#!/usr/bin/env python3

import subprocess
import sys
import os
import time

# Configurar PATH
os.environ['PATH'] = f"{os.path.expanduser('~')}/.local/bin:{os.environ.get('PATH', '')}"

def test_backend():
    print("=== Testando Backend ===")
    
    # Mudar para diretório do backend
    backend_dir = "/home/kaua145/Documentos/Projetos/TCC_Leitura_Barras/backend"
    os.chdir(backend_dir)
    
    try:
        # Iniciar servidor
        print("Iniciando servidor FastAPI...")
        process = subprocess.Popen([
            sys.executable, "main.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Aguardar um pouco para o servidor iniciar
        time.sleep(3)
        
        # Verificar se está rodando
        if process.poll() is None:
            print("✅ Backend iniciado com sucesso!")
            print("🌐 Servidor rodando em: http://localhost:8000")
            print("📋 Documentação da API: http://localhost:8000/docs")
            print("\nPara parar o servidor, pressione Ctrl+C")
            
            # Manter rodando
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Parando servidor...")
                process.terminate()
                process.wait()
        else:
            stdout, stderr = process.communicate()
            print("❌ Erro ao iniciar backend:")
            print("STDOUT:", stdout.decode())
            print("STDERR:", stderr.decode())
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_backend()