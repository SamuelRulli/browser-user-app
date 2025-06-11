# 📁 Estrutura do Projeto - Browser Use API

## 🎯 Visão Geral
Este projeto implementa uma API REST completa para interagir com o serviço Browser Use, permitindo executar tasks de automação de browser via HTTP/JSON.

## 📂 Estrutura de Arquivos

```
browser-user-app/
├── app/
│   ├── main.py              # Script original (mantido para referência)
│   └── api.py               # API Flask principal ⭐
├── ssl/                     # Certificados SSL (criado automaticamente)
│   ├── cert.pem
│   └── key.pem
├── requirements.txt         # Dependências Python ⭐
├── Dockerfile              # Imagem Docker da aplicação ⭐
├── docker-compose.yml      # Orquestração de containers ⭐
├── nginx.conf              # Configuração do Nginx ⭐
├── .dockerignore           # Arquivos ignorados no build
├── .env.example            # Exemplo de configuração ⭐
├── deploy.sh               # Script automatizado de deploy ⭐
├── run_server.py           # Script para iniciar servidor local
├── test_api.py             # Testes automatizados
├── postman_collection.json # Coleção Postman para testes
├── README.md               # Documentação principal ⭐
├── USAGE.md                # Guia de uso detalhado
├── DEPLOY.md               # Guia de deploy completo ⭐
└── PROJECT_STRUCTURE.md    # Este arquivo
```

## 🔧 Arquivos Principais

### 1. `app/api.py` - API Flask Principal
**Funcionalidade:** API REST completa com todos os endpoints
**Endpoints implementados:**
- `POST /api/v1/run-task` - Executar tasks
- `GET /api/v1/task/{id}` - Obter detalhes da task
- `GET /api/v1/task/{id}/status` - Status da task
- `PUT /api/v1/task/{id}/stop` - Parar task
- `PUT /api/v1/task/{id}/pause` - Pausar task
- `PUT /api/v1/task/{id}/resume` - Resumir task
- `GET /api/v1/tasks` - Listar tasks
- `GET /api/v1/task/{id}/media` - Mídia da task
- `GET /api/v1/task/{id}/screenshots` - Screenshots
- `GET /api/v1/task/{id}/gif` - GIF da execução
- `GET /api/v1/task/{id}/wait` - Aguardar conclusão
- `GET /health` - Health check

### 2. `docker-compose.yml` - Orquestração
**Serviços configurados:**
- `browser-use-api`: Aplicação principal
- `nginx`: Proxy reverso (opcional)
- `redis`: Cache para futuras funcionalidades (opcional)

**Profiles disponíveis:**
- Padrão: Apenas API
- `nginx`: API + Nginx
- `cache`: API + Redis

### 3. `Dockerfile` - Imagem da Aplicação
**Características:**
- Base: Python 3.11-slim
- Usuário não-root para segurança
- Health check integrado
- Otimizado para produção

### 4. `nginx.conf` - Proxy Reverso
**Recursos:**
- Rate limiting (10 req/s)
- Compressão GZIP
- Headers de segurança
- SSL/TLS configurado
- CORS habilitado
- Redirecionamento HTTP → HTTPS

### 5. `deploy.sh` - Script de Deploy
**Funcionalidades:**
- Deploy básico (apenas API)
- Deploy com Nginx
- Deploy completo (API + Nginx + Redis)
- Verificações automáticas
- Criação de certificados SSL
- Menu interativo

## 🚀 Modos de Deploy

### 1. Desenvolvimento Local
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar API key
export BROWSER_USE_API_KEY="sua_key"

# Executar
python run_server.py
```

### 2. Docker Básico
```bash
# Configurar .env
cp .env .env

# Deploy
./deploy.sh basic
```

### 3. Produção com HTTPS
```bash
# Configurar domínio no nginx.conf
# Configurar certificados SSL
./deploy.sh nginx
```

## 🔧 Configurações

### Variáveis de Ambiente (.env)
```bash
BROWSER_USE_API_KEY=bu_sua_api_key_aqui  # Obrigatório
PORT=5000                                # Opcional
DEBUG=false                              # Opcional
```

### Portas Utilizadas
- `5000`: API principal
- `80`: HTTP (Nginx)
- `443`: HTTPS (Nginx)
- `6379`: Redis (opcional)

## 🧪 Testes

### 1. Testes Automatizados
```bash
python test_api.py
```

### 2. Postman
- Importar `postman_collection.json`
- Configurar variáveis `base_url` e `task_id`

### 3. cURL
```bash
# Health check
curl -X GET http://localhost:5000/health

# Executar task
curl -X POST http://localhost:5000/api/v1/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Sua task aqui"}'
```

## 📊 Monitoramento

### Logs
```bash
# Docker Compose
docker-compose logs -f

# Apenas API
docker-compose logs -f browser-use-api

# Nginx
docker-compose logs -f nginx
```

### Status
```bash
# Containers
docker-compose ps

# Recursos
docker stats

# Health check
curl http://localhost:5000/health
```

## 🔐 Segurança

### Implementado
- Usuário não-root no container
- Rate limiting no Nginx
- Headers de segurança
- CORS configurado
- SSL/TLS suportado
- Validação de entrada

### Recomendações Adicionais
- Firewall configurado
- Certificados SSL válidos
- Backup regular
- Monitoramento de logs
- Atualizações regulares

## 🚨 Solução de Problemas

### Logs de Debug
```bash
# Informações do sistema
./deploy.sh  # Opção 4 - Verificar status

# Logs detalhados
docker-compose logs --tail=100 browser-use-api

# Teste de conectividade
curl -v http://localhost:5000/health
```

### Problemas Comuns
1. **API Key inválida**: Verificar .env
2. **Porta ocupada**: Alterar PORT no .env
3. **SSL não funciona**: Verificar certificados em ssl/
4. **Container não inicia**: Verificar logs com docker-compose logs

## 📈 Próximos Passos

### Funcionalidades Futuras
- [ ] Autenticação JWT
- [ ] Cache com Redis
- [ ] Métricas com Prometheus
- [ ] Dashboard web
- [ ] Webhook notifications
- [ ] Task scheduling
- [ ] File upload support

### Melhorias de Infraestrutura
- [ ] Kubernetes deployment
- [ ] CI/CD pipeline
- [ ] Load balancing
- [ ] Database persistence
- [ ] Backup automatizado

## 📞 Suporte

### Documentação
- `README.md`: Visão geral e API
- `USAGE.md`: Guia de uso detalhado
- `DEPLOY.md`: Guia de deploy completo

### Recursos Externos
- [Browser Use Docs](https://docs.browser-use.com/)
- [Docker Docs](https://docs.docker.com/)
- [Nginx Docs](https://nginx.org/en/docs/)

## 🎉 Resumo

Este projeto fornece uma solução completa e pronta para produção para interagir com a API Browser Use através de uma interface REST. Com suporte a Docker, HTTPS, monitoramento e deploy automatizado, está preparado para uso em ambientes de desenvolvimento e produção.

**Principais benefícios:**
- ✅ API REST completa
- ✅ Deploy automatizado
- ✅ Configuração flexível
- ✅ Segurança implementada
- ✅ Monitoramento incluído
- ✅ Documentação completa
- ✅ Testes automatizados
- ✅ Suporte a HTTPS
- ✅ Proxy reverso configurado
- ✅ Pronto para produção
