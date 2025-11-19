import json
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada")

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Leitura(Base):
    __tablename__ = "leituras"
    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, index=True)
    descricao = Column(String, default="Não identificado")
    quantidade = Column(Integer, default=1)
    data_hora = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

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
        db = SessionLocal()
        leituras = db.query(Leitura).order_by(Leitura.data_hora.desc()).all()
        
        response = [{
            "id": l.id,
            "codigo_barras": l.codigo_barras,
            "descricao": l.descricao,
            "quantidade": l.quantidade,
            "data_hora": l.data_hora.isoformat()
        } for l in leituras]
        
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