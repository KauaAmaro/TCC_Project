#!/usr/bin/env python3

import os
import sys
import subprocess

def check_dependencies():
    print("=== Verificação de Dependências ===")
    
    # Configurar PATH
    os.environ['PATH'] = f"{os.path.expanduser('~')}/.local/bin:{os.environ.get('PATH', '')}"
    
    deps = [
        ("opencv-python", "cv2"),
        ("pyzbar", "pyzbar"),
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlalchemy", "sqlalchemy")
    ]
    
    for package, module in deps:
        try:
            __import__(module)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - FALTANDO")
            print(f"   Instale com: pip install {package}")

def test_camera_access():
    print("\n=== Teste de Acesso à Câmera ===")
    
    try:
        import cv2
        
        # Testar webcam
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Webcam padrão - OK")
                print(f"   Resolução: {frame.shape}")
            else:
                print("❌ Webcam padrão - Sem frames")
            cap.release()
        else:
            print("❌ Webcam padrão - Não disponível")
        
        # Testar URL de exemplo
        test_url = "http://192.168.1.244:8080/video"
        print(f"\n🔗 Testando URL: {test_url}")
        cap = cv2.VideoCapture(test_url)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print("✅ Stream IP - OK")
                print(f"   Resolução: {frame.shape}")
            else:
                print("❌ Stream IP - Sem frames")
            cap.release()
        else:
            print("❌ Stream IP - Não conectou")
            
    except ImportError:
        print("❌ OpenCV não instalado")

def test_barcode_library():
    print("\n=== Teste da Biblioteca de Códigos ===")
    
    try:
        from pyzbar import pyzbar
        import cv2
        import numpy as np
        
        # Criar imagem de teste simples
        test_image = np.zeros((100, 300), dtype=np.uint8)
        test_image[40:60, 50:250] = 255  # Retângulo branco
        
        # Tentar decodificar (não deve encontrar nada, mas não deve dar erro)
        result = pyzbar.decode(test_image)
        print("✅ pyzbar - Funcionando")
        print(f"   Resultado teste: {len(result)} códigos")
        
    except Exception as e:
        print(f"❌ pyzbar - Erro: {e}")

def main():
    print("🔧 DIAGNÓSTICO DO SISTEMA DE CÓDIGOS DE BARRAS")
    print("=" * 50)
    
    check_dependencies()
    test_camera_access()
    test_barcode_library()
    
    print("\n" + "=" * 50)
    print("💡 PRÓXIMOS PASSOS:")
    print("1. Execute: python3 backend/test_barcode.py")
    print("2. Teste com código de barras real")
    print("3. Verifique logs do backend")

if __name__ == "__main__":
    main()