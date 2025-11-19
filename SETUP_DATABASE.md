# Configuração do Banco de Dados para Vercel

## Problema
O SQLite não funciona no Vercel para operações de escrita (somente leitura). É necessário usar PostgreSQL.

## Solução: Configurar PostgreSQL

### Opção 1: Supabase (Gratuito)
1. Acesse [supabase.com](https://supabase.com)
2. Crie uma conta e um novo projeto
3. Vá em Settings > Database
4. Copie a "Connection string" (URI format)
5. No Vercel, adicione a variável de ambiente:
   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
   ```

### Opção 2: Railway (Gratuito)
1. Acesse [railway.app](https://railway.app)
2. Crie um projeto e adicione PostgreSQL
3. Copie a DATABASE_URL
4. No Vercel, adicione a variável:
   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/railway
   ```

### Opção 3: Neon (Gratuito)
1. Acesse [neon.tech](https://neon.tech)
2. Crie um projeto PostgreSQL
3. Copie a connection string
4. Configure no Vercel

## Configuração no Vercel
1. Vá no dashboard do seu projeto no Vercel
2. Settings > Environment Variables
3. Adicione:
   - Name: `DATABASE_URL`
   - Value: `postgresql://...` (sua string de conexão)
4. Redeploy o projeto

## Teste Local
Para testar localmente com PostgreSQL:
```bash
export DATABASE_URL="postgresql://..."
cd frontend && npm run dev
```

## Estrutura das Tabelas
O sistema criará automaticamente as tabelas:
- `produtos` (id, codigo_barras, descricao, data_cadastro)
- `leituras` (id, codigo_barras, descricao, quantidade, data_hora)