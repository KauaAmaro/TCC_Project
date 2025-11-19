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
        self.active_codes = set()  # Códigos atualmente visíveis
        self.last_detection_time = {}  # Tempo da última detecção por código
        self.detection_timeout = 2.0  # Timeout em segundos para considerar código como "saído"
        
    def start_reading(self, stream_url: str):
        if self.is_reading:
            self.stop_reading()
        
        self.stream_url = stream_url
        self.is_reading = True
        self.active_codes.clear()
        self.last_detection_time.clear()
        self.thread = threading.Thread(target=self._read_stream)
        self.thread.daemon = True
        self.thread.start()
    
    def stop_reading(self):
        self.is_reading = False
        if self.thread:
            self.thread.join()
        self.active_codes.clear()
        self.last_detection_time.clear()
    
    def _read_stream(self):
        cap = cv2.VideoCapture(self.stream_url)
        
        if not cap.isOpened():
            print(f"Erro ao abrir stream: {self.stream_url}")
            return
        
        while self.is_reading:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            
            current_time = time.time()
            detected_codes = set()
            
            # Decodificar códigos de barras no frame atual
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                barcode_data = barcode.data.decode('utf-8')
                detected_codes.add(barcode_data)
                self.last_detection_time[barcode_data] = current_time
            
            # Processar entrada de novos códigos
            new_codes = detected_codes - self.active_codes
            for code in new_codes:
                self._save_barcode_entry(code)
                print(f"ENTRADA: {code}")
            
            # Processar saída de códigos (timeout)
            expired_codes = set()
            for code in list(self.active_codes):
                if code not in detected_codes:
                    # Código não detectado neste frame
                    if current_time - self.last_detection_time.get(code, 0) > self.detection_timeout:
                        expired_codes.add(code)
            
            for code in expired_codes:
                self._save_barcode_exit(code)
                print(f"SAÍDA: {code}")
                self.active_codes.discard(code)
                self.last_detection_time.pop(code, None)
            
            # Atualizar códigos ativos
            self.active_codes = detected_codes.copy()
            
            time.sleep(0.1)  # Pequena pausa para não sobrecarregar
        
        cap.release()
    
    def _save_barcode_entry(self, codigo_barras: str):
        """Registra entrada de um código de barras"""
        db = SessionLocal()
        try:
            existing = db.query(Leitura).filter(Leitura.codigo_barras == codigo_barras).first()
            
            if existing:
                existing.quantidade += 1
                existing.data_hora = datetime.utcnow()
            else:
                leitura = Leitura(codigo_barras=codigo_barras, descricao="Entrada detectada")
                db.add(leitura)
            
            db.commit()
        finally:
            db.close()
    
    def _save_barcode_exit(self, codigo_barras: str):
        """Registra saída de um código de barras"""
        db = SessionLocal()
        try:
            existing = db.query(Leitura).filter(Leitura.codigo_barras == codigo_barras).first()
            
            if existing:
                # Criar novo registro para a saída
                exit_leitura = Leitura(
                    codigo_barras=codigo_barras + "_SAIDA",
                    descricao=f"Saída de {codigo_barras}",
                    quantidade=1
                )
                db.add(exit_leitura)
                db.commit()
        finally:
            db.close()

barcode_reader = BarcodeReader()