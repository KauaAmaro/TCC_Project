import json
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Leitura(Base):
    __tablename__ = "leituras"
    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, index=True)
    descricao = Column(String, default="Não identificado")
    quantidade = Column(Integer, default=1)
    data_hora = Column(DateTime, default=datetime.utcnow)

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
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        db = get_db()
        
        result = db.query(
            Leitura.descricao,
            func.sum(Leitura.quantidade).label('total_quantidade')
        ).group_by(Leitura.descricao).order_by(func.sum(Leitura.quantidade).desc()).all()
        
        response = [{
            "descricao": r.descricao,
            "quantidade": r.total_quantidade
        } for r in result]
        
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