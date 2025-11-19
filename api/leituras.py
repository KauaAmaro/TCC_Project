from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from database_vercel import SessionLocal, Leitura
    from sqlalchemy import func
except ImportError as e:
    print(f"Import error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        try:
            db = SessionLocal()
            leituras = db.query(Leitura).order_by(Leitura.data_hora.desc()).all()
            
            response = [
                {
                    "id": l.id,
                    "codigo_barras": l.codigo_barras,
                    "descricao": l.descricao,
                    "quantidade": l.quantidade,
                    "data_hora": l.data_hora.isoformat()
                }
                for l in leituras
            ]
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
            db.close()
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())