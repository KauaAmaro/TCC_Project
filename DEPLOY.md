# Deploy no Vercel

## Pré-requisitos

1. Conta no [Vercel](https://vercel.com)
2. Conta no [Supabase](https://supabase.com) ou [Railway](https://railway.app) para PostgreSQL
3. Repositório no GitHub

## Configuração do Banco de Dados

### Opção 1: Supabase (Recomendado)
1. Crie um projeto no Supabase
2. Vá em Settings > Database
3. Copie a Connection String (URI)

### Opção 2: Railway
1. Crie um projeto no Railway
2. Adicione PostgreSQL
3. Copie a DATABASE_URL

## Deploy no Vercel

1. **Conectar Repositório**
   - Faça push do código para GitHub
   - Conecte o repositório no Vercel

2. **Configurar Variáveis de Ambiente**
   No painel do Vercel, adicione:
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   ```

3. **Configurações de Build**
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

4. **Deploy**
   - Clique em "Deploy"
   - Aguarde o build completar

## Funcionalidades Limitadas no Vercel

⚠️ **Importante**: No Vercel, as seguintes funcionalidades não estarão disponíveis:

- **Stream de câmera IP**: Serverless functions têm timeout limitado
- **Leitura de códigos de barras em tempo real**: Requer processamento contínuo

### Funcionalidades Disponíveis:
- ✅ Cadastro de produtos
- ✅ Visualização de leituras
- ✅ Relatórios
- ✅ API REST completa

## Alternativas para Stream

Para funcionalidade completa com stream:

1. **Heroku**: Suporta aplicações com processamento contínuo
2. **Railway**: Boa opção para full-stack com background tasks
3. **DigitalOcean App Platform**: Suporte a workers
4. **VPS próprio**: Controle total

## Estrutura Final

```
projeto/
├── frontend/          # Next.js app
├── backend/
│   ├── api/
│   │   └── main.py   # Serverless functions
│   ├── database_vercel.py
│   └── requirements.txt
├── vercel.json
└── DEPLOY.md
```

## Comandos Úteis

```bash
# Testar localmente
cd frontend && npm run dev
cd backend && python3 -m uvicorn api.main:app --reload

# Build para produção
cd frontend && npm run build
```