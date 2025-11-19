#!/usr/bin/env python3
"""
Teste completo da funcionalidade do banco de dados e sistema de cadastro
"""

import sqlite3
import requests
import json
from datetime import datetime
import sys
import os

# Adicionar o diretório backend ao path
sys.path.append('/home/kaua145/Documentos/Projetos/TCC_Leitura_Barras1/backend')

from database import get_db, Leitura, Produto, SessionLocal

def test_database_connection():
    """Testa conexão com o banco de dados"""
    print("🔍 Testando conexão com banco de dados...")
    
    try:
        db_path = "/home/kaua145/Documentos/Projetos/TCC_Leitura_Barras1/backend/leituras.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabelas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ Tabelas encontradas: {[table[0] for table in tables]}")
        
        # Verificar estrutura da tabela leituras
        cursor.execute("PRAGMA table_info(leituras);")
        leituras_columns = cursor.fetchall()
        print(f"✅ Colunas da tabela 'leituras': {[col[1] for col in leituras_columns]}")
        
        # Verificar estrutura da tabela produtos
        cursor.execute("PRAGMA table_info(produtos);")
        produtos_columns = cursor.fetchall()
        print(f"✅ Colunas da tabela 'produtos': {[col[1] for col in produtos_columns]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_database_content():
    """Verifica conteúdo atual do banco"""
    print("\n🔍 Verificando conteúdo atual do banco...")
    
    try:
        db = SessionLocal()
        
        # Contar leituras
        leituras_count = db.query(Leitura).count()
        print(f"📊 Total de leituras: {leituras_count}")
        
        # Mostrar últimas 5 leituras
        if leituras_count > 0:
            ultimas_leituras = db.query(Leitura).order_by(Leitura.data_hora.desc()).limit(5).all()
            print("📋 Últimas 5 leituras:")
            for l in ultimas_leituras:
                print(f"  - {l.codigo_barras} | {l.descricao} | Qtd: {l.quantidade} | {l.data_hora}")
        
        # Contar produtos
        produtos_count = db.query(Produto).count()
        print(f"📦 Total de produtos cadastrados: {produtos_count}")
        
        # Mostrar produtos cadastrados
        if produtos_count > 0:
            produtos = db.query(Produto).order_by(Produto.data_cadastro.desc()).all()
            print("📋 Produtos cadastrados:")
            for p in produtos:
                print(f"  - {p.codigo_barras} | {p.descricao} | {p.data_cadastro}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar conteúdo: {e}")
        return False

def test_direct_database_operations():
    """Testa operações diretas no banco"""
    print("\n🔍 Testando operações diretas no banco...")
    
    try:
        db = SessionLocal()
        
        # Teste 1: Inserir um produto de teste
        test_produto = Produto(
            codigo_barras="TEST123456789",
            descricao="Produto de Teste"
        )
        
        # Verificar se já existe
        existing = db.query(Produto).filter(Produto.codigo_barras == "TEST123456789").first()
        if existing:
            print("⚠️  Produto de teste já existe, removendo...")
            db.delete(existing)
            db.commit()
        
        db.add(test_produto)
        db.commit()
        db.refresh(test_produto)
        print(f"✅ Produto de teste inserido: ID {test_produto.id}")
        
        # Teste 2: Inserir uma leitura de teste
        test_leitura = Leitura(
            codigo_barras="TEST123456789",
            descricao="Produto de Teste",
            quantidade=1
        )
        
        db.add(test_leitura)
        db.commit()
        db.refresh(test_leitura)
        print(f"✅ Leitura de teste inserida: ID {test_leitura.id}")
        
        # Teste 3: Consultar dados inseridos
        produto_verificacao = db.query(Produto).filter(Produto.codigo_barras == "TEST123456789").first()
        leitura_verificacao = db.query(Leitura).filter(Leitura.codigo_barras == "TEST123456789").first()
        
        if produto_verificacao and leitura_verificacao:
            print("✅ Dados de teste verificados com sucesso")
        else:
            print("❌ Falha na verificação dos dados de teste")
        
        # Limpeza: remover dados de teste
        if produto_verificacao:
            db.delete(produto_verificacao)
        if leitura_verificacao:
            db.delete(leitura_verificacao)
        db.commit()
        print("🧹 Dados de teste removidos")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro nas operações diretas: {e}")
        return False

def test_api_endpoints():
    """Testa endpoints da API"""
    print("\n🔍 Testando endpoints da API...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Teste 1: Endpoint raiz
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Endpoint raiz funcionando")
        else:
            print(f"❌ Endpoint raiz falhou: {response.status_code}")
            return False
        
        # Teste 2: Listar leituras
        response = requests.get(f"{base_url}/leituras")
        if response.status_code == 200:
            leituras = response.json()
            print(f"✅ Endpoint /leituras funcionando - {len(leituras)} leituras encontradas")
        else:
            print(f"❌ Endpoint /leituras falhou: {response.status_code}")
        
        # Teste 3: Listar produtos
        response = requests.get(f"{base_url}/produtos")
        if response.status_code == 200:
            produtos = response.json()
            print(f"✅ Endpoint /produtos funcionando - {len(produtos)} produtos encontrados")
        else:
            print(f"❌ Endpoint /produtos falhou: {response.status_code}")
        
        # Teste 4: Cadastrar produto via API
        test_produto_data = {
            "codigo_barras": "API_TEST_789",
            "descricao": "Produto Teste API"
        }
        
        response = requests.post(f"{base_url}/produtos", json=test_produto_data)
        if response.status_code == 200:
            produto_criado = response.json()
            print(f"✅ Produto cadastrado via API: {produto_criado['codigo_barras']}")
            
            # Limpar produto de teste
            # (Nota: seria necessário endpoint DELETE para limpeza completa)
            
        elif response.status_code == 409:
            print("⚠️  Produto já existe (esperado se executado múltiplas vezes)")
        else:
            print(f"❌ Falha ao cadastrar produto: {response.status_code} - {response.text}")
        
        # Teste 5: Relatório
        response = requests.get(f"{base_url}/relatorio")
        if response.status_code == 200:
            relatorio = response.json()
            print(f"✅ Endpoint /relatorio funcionando - {len(relatorio)} itens no relatório")
        else:
            print(f"❌ Endpoint /relatorio falhou: {response.status_code}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API. Certifique-se de que o backend está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erro nos testes da API: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes do sistema de banco de dados e cadastro\n")
    
    tests_passed = 0
    total_tests = 4
    
    # Teste 1: Conexão com banco
    if test_database_connection():
        tests_passed += 1
    
    # Teste 2: Conteúdo do banco
    if test_database_content():
        tests_passed += 1
    
    # Teste 3: Operações diretas
    if test_direct_database_operations():
        tests_passed += 1
    
    # Teste 4: Endpoints da API
    if test_api_endpoints():
        tests_passed += 1
    
    # Resultado final
    print(f"\n📊 RESULTADO DOS TESTES: {tests_passed}/{total_tests} passaram")
    
    if tests_passed == total_tests:
        print("🎉 Todos os testes passaram! O sistema está funcionando corretamente.")
    else:
        print("⚠️  Alguns testes falharam. Verifique os detalhes acima.")
        
        if tests_passed < 3:
            print("\n💡 DICAS:")
            print("- Certifique-se de que o backend está rodando: python backend/main.py")
            print("- Verifique se as dependências estão instaladas: pip install -r backend/requirements.txt")
            print("- Confirme se o arquivo leituras.db existe no diretório backend/")

if __name__ == "__main__":
    main()