#!/bin/bash

echo "=== Sistema de Leitura de Códigos de Barras ==="
echo

# Função para verificar se um comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar dependências
echo "Verificando dependências..."

if ! command_exists python3; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js não encontrado. Instale Node.js 18+"
    exit 1
fi

echo "✅ Dependências OK"
echo

# Instalar dependências do backend
echo "Instalando dependências do backend..."
cd backend
pip3 install -r requirements.txt
cd ..

# Instalar dependências do frontend
echo "Instalando dependências do frontend..."
cd frontend
npm install
cd ..

echo
echo "=== Instruções de Execução ==="
echo
echo "1. Backend (Terminal 1):"
echo "   cd backend && python3 main.py"
echo
echo "2. Frontend (Terminal 2):"
echo "   cd frontend && npm run dev"
echo
echo "3. Acesse: http://localhost:3000"
echo