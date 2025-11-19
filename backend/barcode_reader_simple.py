import cv2
import threading
import time
from pyzbar import pyzbar
from sqlalchemy.orm import Session
from database import SessionLocal, Leitura
from datetime import datetime

class BarcodeReader:
    def __init__(self):
        self.stream_url = None
        self.is_reading = False
        self.thread = None
        
    def start_reading(self, stream_url: str):
        if self.is_reading:
            self.stop_reading()
        
        self.stream_url = stream_url
        self.is_reading = True
        self.thread = threading.Thread(target=self._read_stream)
        self.thread.daemon = True
        self.thread.start()
    
    def stop_reading(self):
        self.is_reading = False
        if self.thread:
            self.thread.join()
    
    def _read_stream(self):
        print(f"🎥 Conectando ao stream: {self.stream_url}")
        cap = cv2.VideoCapture(self.stream_url)
        
        if not cap.isOpened():
            print(f"❌ Erro ao abrir stream: {self.stream_url}")
            return
        
        print("✅ Stream conectado! Iniciando controle de estado...")
        codigos_ativos = set()  # Estado atual dos códigos visíveis
        frame_count = 0
        
        while self.is_reading:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            
            frame_count += 1
            codigos_detectados_agora = set()
            
            try:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                barcodes = pyzbar.decode(gray)
                
                # Coletar todos os códigos detectados neste frame
                for barcode in barcodes:
                    codigo = barcode.data.decode('utf-8')
                    codigos_detectados_agora.add(codigo)
                
            except Exception as e:
                print(f"❌ Erro no frame {frame_count}: {e}")
                continue
            
            # DEBUG: Log do estado atual
            if frame_count % 30 == 0 or codigos_detectados_agora != codigos_ativos:
                print(f"📊 Frame {frame_count} | Ativos: {codigos_ativos} | Detectados: {codigos_detectados_agora}")
            
            # PROCESSAR APENAS NOVAS ENTRADAS (não estavam ativos)
            novas_entradas = codigos_detectados_agora - codigos_ativos
            for codigo in novas_entradas:
                print(f"🎆 REGISTRANDO ENTRADA: {codigo} (frame {frame_count})")
                self._save_barcode(codigo)
            
            # Log de saídas (estavam ativos, mas não detectados agora)
            saidas = codigos_ativos - codigos_detectados_agora
            for codigo in saidas:
                print(f"🚪 SAÍDA DETECTADA: {codigo} (frame {frame_count})")
            
            # ATUALIZAR ESTADO: substituir completamente pelos códigos atuais
            codigos_ativos = codigos_detectados_agora.copy()
            
            time.sleep(0.05)  # Reduzir intervalo para melhor responsividade
        
        print("🛑 Encerrando captura...")
        cap.release()
    
    def _save_barcode(self, codigo_barras: str):
        """Registra código APENAS na primeira detecção (entrada)"""
        from database import Produto
        db = SessionLocal()
        try:
            # Buscar descrição cadastrada
            produto = db.query(Produto).filter(Produto.codigo_barras == codigo_barras).first()
            descricao = produto.descricao if produto else "Não identificado"
            
            existing = db.query(Leitura).filter(Leitura.codigo_barras == codigo_barras).first()
            
            if existing:
                existing.quantidade += 1
                existing.data_hora = datetime.utcnow()
                existing.descricao = descricao  # Atualizar descrição
                print(f"💾 Atualizado: {codigo_barras} ({descricao}) -> Quantidade: {existing.quantidade}")
            else:
                leitura = Leitura(codigo_barras=codigo_barras, descricao=descricao)
                db.add(leitura)
                print(f"🆕 Novo registro: {codigo_barras} ({descricao}) -> Quantidade: 1")
            
            db.commit()
            print(f"✅ Salvo no banco: {codigo_barras}")
        except Exception as e:
            print(f"❌ Erro ao salvar {codigo_barras}: {e}")
            db.rollback()
        finally:
            db.close()

barcode_reader = BarcodeReader()