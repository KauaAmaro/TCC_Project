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
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        try:
            db = SessionLocal()
            
            result = db.query(
                Leitura.descricao,
                func.sum(Leitura.quantidade).label('total_quantidade')
            ).group_by(Leitura.descricao).order_by(func.sum(Leitura.quantidade).desc()).all()
            
            response = [
                {
                    "descricao": r.descricao,
                    "quantidade": r.total_quantidade
                }
                for r in result
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