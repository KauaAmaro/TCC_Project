#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, Leitura
from datetime import datetime

def populate_test_data():
    print("=== POPULANDO DADOS DE TESTE ===")
    
    db = SessionLocal()
    try:
        # Limpar dados existentes
        db.query(Leitura).delete()
        
        # Dados de teste
        test_data = [
            {"codigo_barras": "7891000100103", "descricao": "Água Mineral 500ml", "quantidade": 15},
            {"codigo_barras": "7891000100110", "descricao": "Refrigerante Cola 350ml", "quantidade": 8},
            {"codigo_barras": "7891000100127", "descricao": "Biscoito Chocolate", "quantidade": 12},
            {"codigo_barras": "7891000100134", "descricao": "Leite Integral 1L", "quantidade": 6},
            {"codigo_barras": "7891000100141", "descricao": "Pão de Açúcar", "quantidade": 20},
        ]
        
        for item in test_data:
            leitura = Leitura(
                codigo_barras=item["codigo_barras"],
                descricao=item["descricao"],
                quantidade=item["quantidade"],
                data_hora=datetime.utcnow()
            )
            db.add(leitura)
        
        db.commit()
        print(f"✅ {len(test_data)} registros inseridos com sucesso!")
        
        # Verificar dados inseridos
        total = db.query(Leitura).count()
        print(f"📊 Total de registros no banco: {total}")
        
        # Mostrar dados
        leituras = db.query(Leitura).all()
        for l in leituras:
            print(f"   📦 {l.descricao}: {l.quantidade} leituras")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_test_data()