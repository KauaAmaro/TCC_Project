from sqlalchemy import create_engine, Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./leituras.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Leitura(Base):
    __tablename__ = "leituras"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, index=True)
    descricao = Column(String, default="Não identificado")
    quantidade = Column(Integer, default=1)
    data_hora = Column(DateTime, default=datetime.utcnow)

class Produto(Base):
    __tablename__ = "produtos"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo_barras = Column(String, unique=True, index=True, nullable=False)
    descricao = Column(String, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()