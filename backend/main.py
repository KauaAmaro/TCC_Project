from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db, Leitura, Produto
from barcode_reader_simple import barcode_reader
from typing import List

app = FastAPI(title="Barcode Reader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StreamConfig(BaseModel):
    url: str

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

@app.post("/start-stream")
async def start_stream(config: StreamConfig):
    try:
        barcode_reader.start_reading(config.url)
        return {"message": "Stream iniciado com sucesso", "url": config.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/stop-stream")
async def stop_stream():
    barcode_reader.stop_reading()
    return {"message": "Stream parado"}

@app.get("/leituras", response_model=List[LeituraResponse])
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

@app.get("/relatorio", response_model=List[RelatorioResponse])
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

@app.post("/produtos", response_model=ProdutoResponse)
async def create_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    # Verificar se já existe
    existing = db.query(Produto).filter(Produto.codigo_barras == produto.codigo_barras).first()
    if existing:
        raise HTTPException(status_code=409, detail="Código de barras já cadastrado")
    
    # Criar novo produto
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

@app.get("/produtos", response_model=List[ProdutoResponse])
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

@app.get("/")
async def root():
    return {"message": "Barcode Reader API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)