from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from database_vercel import SessionLocal, Produto
    from datetime import datetime
except ImportError as e:
    print(f"Import error: {e}")

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            db = SessionLocal()
            
            # Check if exists
            existing = db.query(Produto).filter(Produto.codigo_barras == data['codigo_barras']).first()
            if existing:
                self.send_response(409)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"detail": "Código de barras já cadastrado"}).encode())
                db.close()
                return
            
            # Create new product
            db_produto = Produto(
                codigo_barras=data['codigo_barras'].strip(),
                descricao=data['descricao'].strip()
            )
            db.add(db_produto)
            db.commit()
            db.refresh(db_produto)
            
            response = {
                "id": db_produto.id,
                "codigo_barras": db_produto.codigo_barras,
                "descricao": db_produto.descricao,
                "data_cadastro": db_produto.data_cadastro.isoformat()
            }
            
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

    def do_GET(self):
        try:
            db = SessionLocal()
            produtos = db.query(Produto).order_by(Produto.data_cadastro.desc()).all()
            
            response = [
                {
                    "id": p.id,
                    "codigo_barras": p.codigo_barras,
                    "descricao": p.descricao,
                    "data_cadastro": p.data_cadastro.isoformat()
                }
                for p in produtos
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