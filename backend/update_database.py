#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, Base, SessionLocal, Produto

def update_database():
    print("=== ATUALIZANDO BANCO DE DADOS ===")
    
    try:
        # Criar todas as tabelas (incluindo a nova tabela produtos)
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas/atualizadas com sucesso!")
        
        # Verificar se a tabela produtos foi criada
        db = SessionLocal()
        try:
            count = db.query(Produto).count()
            print(f"📊 Tabela produtos: {count} registros")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erro ao atualizar banco: {e}")

if __name__ == "__main__":
    update_database()