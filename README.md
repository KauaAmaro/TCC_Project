# Sistema de Leitura de Códigos de Barras

Sistema full-stack para leitura de códigos de barras a partir de stream de câmera IP.

## Estrutura do Projeto

```
TCC_Leitura_Barras/
├── backend/          # API Python + FastAPI
├── frontend/         # Interface Next.js
└── README.md
```

## Pré-requisitos

- Python 3.8+
- Node.js 18+
- Câmera IP com stream acessível

## Instalação e Execução

### 1. Backend (Python + FastAPI)

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python main.py
```

O backend estará disponível em: http://localhost:8000

### 2. Frontend (Next.js)

```bash
cd frontend

# Instalar dependências
npm install

# Executar em modo desenvolvimento
npm run dev
```

O frontend estará disponível em: http://localhost:3000

## Uso do Sistema

1. **Configurar Stream**: Na interface web, insira a URL do stream da câmera IP (ex: `http://192.168.1.244:8080/video`)

2. **Iniciar Leitura**: Clique em "Iniciar Leitura" para começar a capturar códigos de barras

3. **Visualizar Dados**: A tabela será atualizada automaticamente a cada 2 segundos com as leituras

4. **Parar Leitura**: Use o botão "Parar Leitura" quando necessário

## Funcionalidades Avançadas

### Contagem Única por Entrada/Saída

O sistema implementa uma lógica inteligente para evitar contagens duplicadas:

- **Entrada**: Quando um código aparece pela primeira vez no campo de visão, é registrado
- **Permanência**: Enquanto o código permanecer visível, não é contado novamente
- **Saída**: Após o código desaparecer e reaparecer, pode ser contado novamente

Isso garante precisão nas contagens, evitando múltiplas detecções do mesmo item.

## API Endpoints

- `GET /leituras` - Lista todas as leituras
- `POST /start-stream` - Inicia leitura do stream
- `POST /stop-stream` - Para a leitura

## Banco de Dados

O sistema usa SQLite (`leituras.db`) com a seguinte estrutura:

- `codigo_barras`: Código lido
- `descricao`: Descrição do produto (padrão: "Não identificado")
- `quantidade`: Contador de leituras do mesmo código
- `data_hora`: Timestamp da última leitura

## Configuração da Câmera IP

Certifique-se de que sua câmera IP está configurada para fornecer um stream de vídeo acessível via HTTP. Exemplos de URLs comuns:

- `http://IP:8080/video`
- `http://IP/mjpeg`
- `rtsp://IP:554/stream`

## Troubleshooting

- **Erro de CORS**: Verifique se o backend está rodando na porta 8000
- **Stream não funciona**: Teste a URL da câmera em um navegador
- **Códigos não são lidos**: Verifique a qualidade da imagem e iluminação