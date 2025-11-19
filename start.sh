#!/bin/bash

# Configurar PATH para Node.js local
export PATH="/home/kaua145/Documentos/Projetos/TCC_Leitura_Barras/node-v18.18.0-linux-x64/bin:$PATH"

echo "=== Sistema de Leitura de Códigos de Barras ==="
echo "✨ Nova funcionalidade: Contagem única por entrada/saída"
echo
echo "Para executar o sistema:"
echo
echo "1. Backend (Terminal 1):"
echo "   python3 test_backend.py"
echo "   OU manualmente:"
echo "   cd backend && export PATH=\$HOME/.local/bin:\$PATH && python3 main.py"
echo
echo "2. Frontend (Terminal 2):"
echo "   export PATH=\"/home/kaua145/Documentos/Projetos/TCC_Leitura_Barras/node-v18.18.0-linux-x64/bin:\$PATH\""
echo "   cd frontend"
echo "   npm run dev"
echo
echo "3. Acesse: http://localhost:3000"
echo
echo "📋 Funcionalidades implementadas:"
echo "   • Detecção única por entrada de código"
echo "   • Evita contagens duplicadas"
echo "   • Controle de entrada/saída automático"
echo