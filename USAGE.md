# Como Usar a API Browser Use Wrapper

## 🚀 Início Rápido

### 1. Instalação
```bash
# Clone ou baixe os arquivos do projeto
cd browser-user-app

# Instale as dependências
pip install -r requirements.txt
```

### 2. Configuração
```bash
# Configure sua API key do Browser Use
export BROWSER_USE_API_KEY="sua_api_key_aqui"

# Ou crie um arquivo .env baseado no .env
cp .env .env
# Edite o arquivo .env com sua API key
```

### 3. Iniciar o Servidor
```bash
# Opção 1: Usando o script dedicado
python run_server.py

# Opção 2: Diretamente
python app/api.py
```

O servidor estará disponível em `http://localhost:5000`

### 4. Testar a API
```bash
# Teste básico
python test_api.py

# Ou teste manual
curl -X GET http://localhost:5000/health
```

## 📱 Usando com Postman

### Importar Coleção
1. Abra o Postman
2. Clique em "Import"
3. Selecione o arquivo `postman_collection.json`
4. A coleção "Browser Use API" será importada

### Configurar Variáveis
1. Na coleção, vá em "Variables"
2. Configure:
   - `base_url`: `http://localhost:5000`
   - `task_id`: (será preenchido automaticamente após criar uma task)

### Exemplos de Uso

#### Exemplo 1: Task Simples
```json
POST /api/v1/run-task
{
  "task": "Vá para https://httpbin.org/get e me mostre o conteúdo da resposta"
}
```

#### Exemplo 2: Task com Aguardo
```json
POST /api/v1/run-task
{
  "task": "Abra https://www.google.com e pesquise por 'Python'",
  "wait_for_completion": true,
  "timeout": 120
}
```

#### Exemplo 3: Task com Output Estruturado
```json
POST /api/v1/run-task
{
  "task": "Vá para https://news.ycombinator.com e extraia os títulos das 5 primeiras notícias",
  "structured_output_json": "{\"titles\": [\"string\"]}",
  "wait_for_completion": true
}
```

## 🔄 Fluxos de Trabalho

### Fluxo Assíncrono (Recomendado)
1. **Criar Task**
   ```
   POST /api/v1/run-task
   Body: {"task": "sua task aqui"}
   ```
   
2. **Monitorar Status**
   ```
   GET /api/v1/task/{task_id}/status
   ```
   
3. **Obter Resultado**
   ```
   GET /api/v1/task/{task_id}
   ```

### Fluxo Síncrono (Para tasks rápidas)
1. **Criar e Aguardar**
   ```
   POST /api/v1/run-task
   Body: {
     "task": "sua task aqui",
     "wait_for_completion": true,
     "timeout": 300
   }
   ```

## 📊 Monitoramento

### Verificar Status
```bash
curl -X GET http://localhost:5000/api/v1/task/{task_id}/status
```

### Listar Todas as Tasks
```bash
curl -X GET "http://localhost:5000/api/v1/tasks?limit=10&offset=0"
```

### Obter Screenshots
```bash
curl -X GET http://localhost:5000/api/v1/task/{task_id}/screenshots
```

## 🛠️ Controle de Tasks

### Parar Task
```bash
curl -X PUT http://localhost:5000/api/v1/task/{task_id}/stop
```

### Pausar Task
```bash
curl -X PUT http://localhost:5000/api/v1/task/{task_id}/pause
```

### Resumir Task
```bash
curl -X PUT http://localhost:5000/api/v1/task/{task_id}/resume
```

## 🔧 Configurações Avançadas

### Parâmetros Disponíveis para run-task

```json
{
  "task": "string (obrigatório)",
  "secrets": {},
  "allowed_domains": ["string"],
  "save_browser_data": true,
  "structured_output_json": "string",
  "llm_model": "gpt-4o",
  "use_adblock": true,
  "use_proxy": true,
  "proxy_country_code": "us",
  "highlight_elements": true,
  "included_file_names": ["string"],
  "wait_for_completion": false,
  "timeout": 300
}
```

### Modelos LLM Disponíveis
- `gpt-4o` (padrão)
- `gpt-4o-mini`
- `gpt-4.1`
- `gpt-4.1-mini`
- `gemini-2.0-flash`
- `gemini-2.0-flash-lite`
- `claude-3-7-sonnet-20250219`
- `claude-sonnet-4-20250514`
- `llama-4-maverick-17b-128e-instruct`

### Códigos de País para Proxy
- `us` (padrão)
- `uk`
- `fr`
- `it`
- `jp`
- `au`
- `de`
- `fi`
- `ca`

## 🚨 Tratamento de Erros

### Códigos de Status HTTP
- `200`: Sucesso
- `400`: Erro de validação
- `404`: Recurso não encontrado
- `408`: Timeout
- `500`: Erro interno

### Exemplos de Respostas de Erro
```json
{
  "error": "Campo 'task' é obrigatório"
}
```

```json
{
  "task_id": "task_123",
  "status": "timeout",
  "error": "Task não foi concluída em 300 segundos",
  "partial_result": {...}
}
```

## 💡 Dicas e Boas Práticas

### Para Tasks Longas
- Use `wait_for_completion: false`
- Monitore o status periodicamente
- Configure um timeout adequado

### Para Tasks Rápidas
- Use `wait_for_completion: true`
- Configure timeout menor (30-120 segundos)

### Segurança
- Mantenha sua API key segura
- Use `allowed_domains` para restringir acesso
- Use `secrets` para dados sensíveis

### Performance
- Use `use_adblock: true` para páginas mais rápidas
- Configure `proxy_country_code` próximo ao target
- Use `structured_output_json` para dados estruturados

## 🐛 Solução de Problemas

### API não inicia
```bash
# Verifique se as dependências estão instaladas
pip install -r requirements.txt

# Verifique se a porta está livre
lsof -ti:5000

# Inicie com debug
DEBUG=true python run_server.py
```

### Erro de API Key
```bash
# Verifique se a API key está configurada
echo $BROWSER_USE_API_KEY

# Configure a API key
export BROWSER_USE_API_KEY="sua_api_key_aqui"
```

### Task falha
- Verifique se o domínio está em `allowed_domains`
- Verifique se a task está bem descrita
- Tente com um modelo LLM diferente

## 📞 Suporte

Para mais informações:
- Documentação oficial: https://docs.browser-use.com/
- README.md do projeto
- Arquivo de exemplo: postman_collection.json
