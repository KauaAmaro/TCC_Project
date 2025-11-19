from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database_vercel import get_db, Leitura, Produto

app = FastAPI(title="Barcode Reader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeituraResponse(BaseModel):
    id: int
    codigo_barras: str
    descricao: str
    quantidade: int
    data_hora: str

class RelatorioResponse(BaseModel):
    descricao: str
    quantidade: int

class ProdutoCreate(BaseModel):
    codigo_barras: str
    descricao: str

class ProdutoResponse(BaseModel):
    id: int
    codigo_barras: str
    descricao: str
    data_cadastro: str

@app.get("/api/leituras", response_model=List[LeituraResponse])
async def get_leituras(db: Session = Depends(get_db)):
    leituras = db.query(Leitura).order_by(Leitura.data_hora.desc()).all()
    return [
        LeituraResponse(
            id=l.id,
            codigo_barras=l.codigo_barras,
            descricao=l.descricao,
            quantidade=l.quantidade,
            data_hora=l.data_hora.isoformat()
        )
        for l in leituras
    ]

@app.get("/api/relatorio", response_model=List[RelatorioResponse])
async def get_relatorio(db: Session = Depends(get_db)):
    from sqlalchemy import func
    
    result = db.query(
        Leitura.descricao,
        func.sum(Leitura.quantidade).label('total_quantidade')
    ).group_by(Leitura.descricao).order_by(func.sum(Leitura.quantidade).desc()).all()
    
    return [
        RelatorioResponse(
            descricao=r.descricao,
            quantidade=r.total_quantidade
        )
        for r in result
    ]

@app.post("/api/produtos", response_model=ProdutoResponse)
async def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    existing = db.query(Produto).filter(Produto.codigo_barras == produto.codigo_barras).first()
    if existing:
        raise HTTPException(status_code=409, detail="Código de barras já cadastrado")
    
    db_produto = Produto(
        codigo_barras=produto.codigo_barras.strip(),
        descricao=produto.descricao.strip()
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    
    return ProdutoResponse(
        id=db_produto.id,
        codigo_barras=db_produto.codigo_barras,
        descricao=db_produto.descricao,
        data_cadastro=db_produto.data_cadastro.isoformat()
    )

@app.get("/api/produtos", response_model=List[ProdutoResponse])
async def get_produtos(db: Session = Depends(get_db)):
    produtos = db.query(Produto).order_by(Produto.data_cadastro.desc()).all()
    return [
        ProdutoResponse(
            id=p.id,
            codigo_barras=p.codigo_barras,
            descricao=p.descricao,
            data_cadastro=p.data_cadastro.isoformat()
        )
        for p in produtos
    ]

@app.post("/api/leituras")
async def create_leitura(codigo_barras: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.codigo_barras == codigo_barras).first()
    descricao = produto.descricao if produto else "Não identificado"
    
    existing = db.query(Leitura).filter(Leitura.codigo_barras == codigo_barras).first()
    
    if existing:
        existing.quantidade += 1
        existing.data_hora = datetime.utcnow()
        db.commit()
        return {"message": "Leitura atualizada"}
    else:
        nova_leitura = Leitura(
            codigo_barras=codigo_barras,
            descricao=descricao,
            quantidade=1
        )
        db.add(nova_leitura)
        db.commit()
        return {"message": "Nova leitura registrada"}

@app.get("/api")
async def root():
    return {"message": "Barcode Reader API - Vercel"}