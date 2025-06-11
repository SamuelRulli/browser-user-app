# 🚀 Guia de Deploy - Browser Use API

Este guia explica como fazer o deploy da API Browser Use usando Docker Compose em um servidor.

## 📋 Pré-requisitos

### No Servidor
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git (para clonar o repositório)
- Porta 5000 disponível (ou configurar outra)
- Para HTTPS: Porta 80 e 443 disponíveis

### Verificar Instalação
```bash
docker --version
docker-compose --version
```

## 🔧 Configuração Inicial

### 1. Clonar/Copiar Arquivos
```bash
# Se usando Git
git clone <seu-repositorio>
cd browser-user-app

# Ou copie os arquivos manualmente para o servidor
```

### 2. Configurar Variáveis de Ambiente
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar configurações
nano .env
```

**Configurações obrigatórias no .env:**
```bash
# API Key do Browser Use (OBRIGATÓRIO)
BROWSER_USE_API_KEY=bu_sua_api_key_aqui

# Configurações opcionais
PORT=5000
DEBUG=false
```

### 3. Configurar Domínio (Para HTTPS)
Se você vai usar HTTPS com domínio próprio, edite o arquivo `nginx.conf`:
```bash
nano nginx.conf
```

Altere a linha:
```nginx
server_name api.yourdomain.com;
```

Para seu domínio real:
```nginx
server_name api.seudominio.com;
```

## 🚀 Opções de Deploy

### Opção 1: Deploy Básico (Recomendado para início)
Apenas a API, sem proxy reverso:
```bash
./deploy.sh basic
```

**Acesso:**
- API: `http://seu-servidor:5000`
- Health Check: `http://seu-servidor:5000/health`

### Opção 2: Deploy com Nginx
API + Proxy Reverso + HTTPS:
```bash
./deploy.sh nginx
```

**Recursos inclusos:**
- Rate limiting
- Compressão GZIP
- Headers de segurança
- Redirecionamento HTTP → HTTPS
- Certificados SSL auto-assinados (para teste)

**Acesso:**
- API: `https://seu-servidor` ou `https://seudominio.com`
- Health Check: `https://seu-servidor/health`

### Opção 3: Deploy Completo
API + Nginx + Redis (para futuras funcionalidades):
```bash
./deploy.sh full
```

## 🔒 Configuração SSL/HTTPS

### Para Desenvolvimento/Teste
O script cria certificados auto-assinados automaticamente.

### Para Produção
1. **Obter certificados válidos:**
   ```bash
   # Usando Let's Encrypt (certbot)
   sudo apt install certbot
   sudo certbot certonly --standalone -d seudominio.com
   
   # Copiar certificados
   mkdir -p ssl
   sudo cp /etc/letsencrypt/live/seudominio.com/fullchain.pem ssl/cert.pem
   sudo cp /etc/letsencrypt/live/seudominio.com/privkey.pem ssl/key.pem
   sudo chown $USER:$USER ssl/*.pem
   ```

2. **Ou usar certificados próprios:**
   ```bash
   mkdir -p ssl
   # Copie seus certificados para:
   # ssl/cert.pem (certificado)
   # ssl/key.pem (chave privada)
   ```

## 🔧 Comandos de Gerenciamento

### Verificar Status
```bash
docker-compose ps
```

### Ver Logs
```bash
# Todos os serviços
docker-compose logs -f

# Apenas API
docker-compose logs -f browser-use-api

# Apenas Nginx
docker-compose logs -f nginx
```

### Restart Serviços
```bash
# Todos
docker-compose restart

# Apenas API
docker-compose restart browser-use-api
```

### Parar Serviços
```bash
docker-compose down
```

### Atualizar Aplicação
```bash
# Parar serviços
docker-compose down

# Rebuild
docker-compose build --no-cache browser-use-api

# Reiniciar
docker-compose up -d
```

### Limpar Tudo
```bash
# Remove containers, volumes e imagens
docker-compose down -v --rmi all
```

## 🧪 Testes Pós-Deploy

### 1. Health Check
```bash
curl -X GET http://localhost:5000/health
# ou
curl -X GET https://seudominio.com/health
```

### 2. Teste de API
```bash
curl -X POST http://localhost:5000/api/v1/run-task \
  -H "Content-Type: application/json" \
  -d '{"task": "Vá para https://httpbin.org/get e me mostre o resultado"}'
```

### 3. Script de Teste
```bash
python test_api.py
```

## 🔍 Monitoramento

### Verificar Recursos
```bash
# CPU e Memória dos containers
docker stats

# Espaço em disco
df -h
docker system df
```

### Logs de Sistema
```bash
# Logs do Docker
journalctl -u docker.service

# Logs da aplicação
docker-compose logs --tail=100 browser-use-api
```

## 🚨 Solução de Problemas

### API não inicia
```bash
# Verificar logs
docker-compose logs browser-use-api

# Verificar configuração
cat .env

# Verificar porta
netstat -tlnp | grep :5000
```

### Erro de API Key
```bash
# Verificar se está configurada
grep BROWSER_USE_API_KEY .env

# Testar API key manualmente
curl -H "Authorization: Bearer sua_api_key" \
  https://api.browser-use.com/api/v1/ping
```

### Problemas de SSL
```bash
# Verificar certificados
ls -la ssl/
openssl x509 -in ssl/cert.pem -text -noout

# Testar SSL
openssl s_client -connect seudominio.com:443
```

### Container não consegue resolver DNS
```bash
# Adicionar DNS no docker-compose.yml
services:
  browser-use-api:
    dns:
      - 8.8.8.8
      - 8.8.4.4
```

## 🔧 Configurações Avançadas

### Alterar Porta
No arquivo `.env`:
```bash
PORT=8080
```

No `docker-compose.yml`:
```yaml
ports:
  - "8080:8080"
```

### Configurar Rate Limiting
No `nginx.conf`, altere:
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

### Adicionar Autenticação
Você pode adicionar autenticação básica no Nginx:
```nginx
location /api/ {
    auth_basic "API Access";
    auth_basic_user_file /etc/nginx/.htpasswd;
    # ... resto da configuração
}
```

### Backup Automático
Criar script de backup:
```bash
#!/bin/bash
# backup.sh
docker-compose exec browser-use-api tar czf - /app > backup-$(date +%Y%m%d).tar.gz
```

## 📊 Métricas e Logs

### Estrutura de Logs
```
/var/log/nginx/access.log  # Logs de acesso Nginx
/var/log/nginx/error.log   # Logs de erro Nginx
```

### Rotação de Logs
Configure logrotate:
```bash
sudo nano /etc/logrotate.d/docker-compose
```

```
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=1M
    missingok
    delaycompress
    copytruncate
}
```

## 🔐 Segurança

### Firewall
```bash
# Permitir apenas portas necessárias
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### Atualizações
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade

# Atualizar Docker
sudo apt update docker-ce docker-ce-cli containerd.io
```

### Backup da Configuração
```bash
# Fazer backup dos arquivos importantes
tar czf browser-use-backup.tar.gz \
  .env docker-compose.yml nginx.conf ssl/
```

## 📞 Suporte

### Logs Úteis para Debug
```bash
# Coletar informações para suporte
echo "=== System Info ===" > debug.log
uname -a >> debug.log
docker --version >> debug.log
docker-compose --version >> debug.log

echo "=== Container Status ===" >> debug.log
docker-compose ps >> debug.log

echo "=== API Logs ===" >> debug.log
docker-compose logs --tail=50 browser-use-api >> debug.log

echo "=== Environment ===" >> debug.log
cat .env | grep -v API_KEY >> debug.log
```

### Contatos
- Documentação Browser Use: https://docs.browser-use.com/
- Issues do projeto: (seu repositório)
