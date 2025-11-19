#!/usr/bin/env python3

import cv2
from pyzbar import pyzbar
import sys

def test_barcode_detection():
    print("=== Teste de Detecção de Códigos de Barras ===")
    
    # Testar com webcam padrão primeiro
    print("1. Testando webcam padrão (índice 0)...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Webcam não disponível, testando com URL de exemplo...")
        # Testar com URL de exemplo
        test_url = "http://192.168.1.244:8080/video"
        cap = cv2.VideoCapture(test_url)
        
        if not cap.isOpened():
            print(f"❌ Não foi possível conectar a {test_url}")
            print("💡 Dicas:")
            print("   - Verifique se a câmera IP está ligada")
            print("   - Teste a URL no navegador")
            print("   - Verifique a rede")
            return
    
    print("✅ Câmera conectada!")
    
    frame_count = 0
    detection_count = 0
    
    try:
        while frame_count < 100:  # Testar 100 frames
            ret, frame = cap.read()
            if not ret:
                print("❌ Falha ao capturar frame")
                break
            
            frame_count += 1
            
            # Converter para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Tentar detectar códigos
            barcodes = pyzbar.decode(gray)
            
            if barcodes:
                detection_count += 1
                print(f"🎯 Frame {frame_count}: {len(barcodes)} código(s) detectado(s)")
                for barcode in barcodes:
                    data = barcode.data.decode('utf-8')
                    type_name = barcode.type
                    print(f"   📊 {data} ({type_name})")
            
            elif frame_count % 20 == 0:
                print(f"🔍 Frame {frame_count}: Nenhum código detectado")
            
            # Mostrar frame (opcional)
            cv2.imshow('Teste Barcode', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido pelo usuário")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        
        print(f"\n📈 Resultado do teste:")
        print(f"   Frames processados: {frame_count}")
        print(f"   Detecções: {detection_count}")
        print(f"   Taxa de detecção: {detection_count/frame_count*100:.1f}%")

if __name__ == "__main__":
    test_barcode_detection()