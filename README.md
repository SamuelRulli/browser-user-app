# Browser Use API Wrapper

Esta aplicação Flask fornece uma API REST para interagir com o serviço Browser Use, permitindo executar tasks de automação de browser via Postman ou qualquer cliente HTTP.

## Instalação

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Configure sua API key do Browser Use:
```bash
export BROWSER_USE_API_KEY="sua_api_key_aqui"
```

3. Execute a aplicação:
```bash
python app/api.py
```

A API estará disponível em `http://localhost:5000`

## Endpoints Disponíveis

### 1. Health Check
```
GET /health
```
Verifica se a API está funcionando.

### 2. Executar Task
```
POST /api/v1/run-task
```

**Body (JSON):**
```json
{
  "task": "Abra https://www.google.com e pesquise por 'OpenAI'",
  "wait_for_completion": false,
  "timeout": 300,
  "llm_model": "gpt-4o",
  "use_adblock": true,
  "use_proxy": true,
  "proxy_country_code": "us",
  "highlight_elements": true,
  "save_browser_data": false,
  "secrets": {},
  "allowed_domains": ["google.com"],
  "structured_output_json": null,
  "included_file_names": []
}
```

**Parâmetros:**
- `task` (obrigatório): Descrição da task a ser executada
- `wait_for_completion` (opcional): Se `true`, aguarda a conclusão antes de retornar
- `timeout` (opcional): Timeout em segundos para aguardar conclusão (padrão: 300)
- Outros parâmetros seguem a documentação oficial da Browser Use API

**Resposta (wait_for_completion=false):**
```json
{
  "task_id": "task_123456",
  "status": "created",
  "message": "Task criada com sucesso. Use /api/v1/task/{task_id} para acompanhar o progresso."
}
```

**Resposta (wait_for_completion=true):**
```json
{
  "task_id": "task_123456",
  "status": "completed",
  "result": {
    "id": "task_123456",
    "task": "Abra https://www.google.com e pesquise por 'OpenAI'",
    "output": "Resultado da pesquisa...",
    "status": "finished",
    "created_at": "2023-11-07T05:31:56Z",
    "finished_at": "2023-11-07T05:32:30Z",
    "steps": [...],
    "live_url": "https://...",
    "browser_data": {...},
    "output_files": [...]
  }
}
```

### 3. Obter Detalhes da Task
```
GET /api/v1/task/{task_id}
```

Retorna todos os detalhes da task, incluindo steps, output, status, etc.

### 4. Obter Status da Task
```
GET /api/v1/task/{task_id}/status
```

Retorna apenas o status atual da task.

### 5. Aguardar Conclusão
```
GET /api/v1/task/{task_id}/wait?timeout=300&poll_interval=2
```

Aguarda a conclusão de uma task específica.

### 6. Controle de Tasks
```
PUT /api/v1/task/{task_id}/stop    # Para a task
PUT /api/v1/task/{task_id}/pause   # Pausa a task
PUT /api/v1/task/{task_id}/resume  # Resume a task
```

### 7. Listar Tasks
```
GET /api/v1/tasks?limit=10&offset=0
```

Lista todas as tasks do usuário.

### 8. Mídia e Screenshots
```
GET /api/v1/task/{task_id}/media        # Obtém mídia da task
GET /api/v1/task/{task_id}/screenshots  # Obtém screenshots
GET /api/v1/task/{task_id}/gif          # Obtém GIF da execução
```

## Exemplos de Uso com Postman

### Exemplo 1: Task Simples (Assíncrona)
```
POST http://localhost:5000/api/v1/run-task
Content-Type: application/json

{
  "task": "Vá para https://httpbin.org/get e copie o conteúdo da resposta JSON"
}
```

### Exemplo 2: Task com Aguardo de Conclusão
```
POST http://localhost:5000/api/v1/run-task
Content-Type: application/json

{
  "task": "Abra https://www.google.com, pesquise por 'Python Flask' e me diga quantos resultados foram encontrados",
  "wait_for_completion": true,
  "timeout": 120
}
```

### Exemplo 3: Task com Output Estruturado
```
POST http://localhost:5000/api/v1/run-task
Content-Type: application/json

{
  "task": "Vá para https://news.ycombinator.com e extraia os títulos das 5 primeiras notícias",
  "structured_output_json": "{\"titles\": [\"string\"]}",
  "wait_for_completion": true
}
```

### Exemplo 4: Verificar Status de Task
```
GET http://localhost:5000/api/v1/task/task_123456/status
```

### Exemplo 5: Obter Resultado Completo
```
GET http://localhost:5000/api/v1/task/task_123456
```

## Fluxo de Trabalho Recomendado

1. **Executar Task Assíncrona:**
   ```
   POST /api/v1/run-task
   ```
   
2. **Monitorar Status:**
   ```
   GET /api/v1/task/{task_id}/status
   ```
   
3. **Obter Resultado Final:**
   ```
   GET /api/v1/task/{task_id}
   ```

Ou alternativamente:

1. **Executar Task Síncrona:**
   ```
   POST /api/v1/run-task (com wait_for_completion=true)
   ```

## Status Possíveis

- `created`: Task foi criada mas ainda não iniciou
- `running`: Task está em execução
- `finished`: Task foi concluída com sucesso
- `failed`: Task falhou
- `stopped`: Task foi parada manualmente
- `paused`: Task está pausada

## Tratamento de Erros

A API retorna códigos de status HTTP apropriados:

- `200`: Sucesso
- `400`: Erro de validação (ex: campo obrigatório ausente)
- `404`: Task não encontrada
- `408`: Timeout (quando wait_for_completion=true)
- `500`: Erro interno

Exemplo de resposta de erro:
```json
{
  "error": "Campo 'task' é obrigatório"
}
```

## Configuração Avançada

### Variáveis de Ambiente

- `BROWSER_USE_API_KEY`: Sua API key do Browser Use
- `PORT`: Porta da aplicação (padrão: 5000)
- `DEBUG`: Modo debug (padrão: False)

### Exemplo com Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
EXPOSE 5000

ENV BROWSER_USE_API_KEY=sua_api_key_aqui
CMD ["python", "app/api.py"]
```

## Segurança

- Mantenha sua API key segura e não a exponha em código
- Use HTTPS em produção
- Configure `allowed_domains` para restringir acesso a domínios específicos
- Use `secrets` para dados sensíveis que precisam ser passados para a task

## Suporte

Para mais informações sobre os parâmetros e funcionalidades, consulte a documentação oficial da Browser Use API: https://docs.browser-use.com/
