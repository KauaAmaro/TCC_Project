import json
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

def get_db():
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não configurada no Vercel")
    
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def handler(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        db = get_db()
        
        if request.method == 'POST':
            data = json.loads(request.body)
            
            existing = db.query(Produto).filter(Produto.codigo_barras == data['codigo_barras']).first()
            if existing:
                return {
                    'statusCode': 409,
                    'headers': headers,
                    'body': json.dumps({"detail": "Código de barras já cadastrado"})
                }
            
            produto = Produto(
                codigo_barras=data['codigo_barras'].strip(),
                descricao=data['descricao'].strip()
            )
            db.add(produto)
            db.commit()
            db.refresh(produto)
            
            response = {
                "id": produto.id,
                "codigo_barras": produto.codigo_barras,
                "descricao": produto.descricao,
                "data_cadastro": produto.data_cadastro.isoformat()
            }
            
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps(response)}
        
        elif request.method == 'GET':
            produtos = db.query(Produto).order_by(Produto.data_cadastro.desc()).all()
            response = [{
                "id": p.id,
                "codigo_barras": p.codigo_barras,
                "descricao": p.descricao,
                "data_cadastro": p.data_cadastro.isoformat()
            } for p in produtos]
            
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps(response)}
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"error": str(e)})
        }
    finally:
        if 'db' in locals():
            db.close()