#!/bin/bash

# Script de deploy para Browser Use API
# Uso: ./deploy.sh [ambiente]

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Verificar se Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        error "Docker não está instalado. Instale o Docker primeiro."
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose não está instalado. Instale o Docker Compose primeiro."
    fi
    
    log "Docker e Docker Compose encontrados ✓"
}

# Verificar arquivo .env
check_env() {
    if [ ! -f .env ]; then
        warn "Arquivo .env não encontrado. Criando a partir do .env.example..."
        if [ -f .env ]; then
            cp .env .env
            warn "Edite o arquivo .env com suas configurações antes de continuar!"
            warn "Especialmente a BROWSER_USE_API_KEY"
            read -p "Pressione Enter para continuar após editar o .env..."
        else
            error "Arquivo .env.example não encontrado!"
        fi
    fi
    
    # Verificar se API key está configurada
    if ! grep -q "BROWSER_USE_API_KEY=bu_" .env; then
        warn "BROWSER_USE_API_KEY não parece estar configurada corretamente no .env"
        read -p "Deseja continuar mesmo assim? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    log "Arquivo .env verificado ✓"
}

# Build da aplicação
build_app() {
    log "Fazendo build da aplicação..."
    docker-compose build --no-cache browser-use-api
    log "Build concluído ✓"
}

# Deploy básico (apenas API)
deploy_basic() {
    log "Iniciando deploy básico (apenas API)..."
    docker-compose up -d browser-use-api
    log "Deploy básico concluído ✓"
}

# Deploy com Nginx
deploy_with_nginx() {
    log "Iniciando deploy com Nginx..."
    
    # Verificar se certificados SSL existem
    if [ ! -d "ssl" ]; then
        warn "Diretório SSL não encontrado. Criando certificados auto-assinados para teste..."
        mkdir -p ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/key.pem \
            -out ssl/cert.pem \
            -subj "/C=BR/ST=State/L=City/O=Organization/CN=localhost"
        warn "Certificados auto-assinados criados. Para produção, use certificados válidos!"
    fi
    
    docker-compose --profile nginx up -d
    log "Deploy com Nginx concluído ✓"
}

# Deploy completo (com Redis)
deploy_full() {
    log "Iniciando deploy completo (API + Nginx + Redis)..."
    
    # Verificar SSL
    if [ ! -d "ssl" ]; then
        warn "Diretório SSL não encontrado. Criando certificados auto-assinados..."
        mkdir -p ssl
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/key.pem \
            -out ssl/cert.pem \
            -subj "/C=BR/ST=State/L=City/O=Organization/CN=localhost"
    fi
    
    docker-compose --profile nginx --profile cache up -d
    log "Deploy completo concluído ✓"
}

# Verificar status dos serviços
check_status() {
    log "Verificando status dos serviços..."
    docker-compose ps
    
    # Aguardar API ficar disponível
    log "Aguardando API ficar disponível..."
    for i in {1..30}; do
        if curl -f http://localhost:5000/health &>/dev/null; then
            log "API está respondendo ✓"
            break
        fi
        if [ $i -eq 30 ]; then
            error "API não respondeu após 30 tentativas"
        fi
        sleep 2
    done
    
    # Mostrar logs se houver erro
    if ! curl -f http://localhost:5000/health &>/dev/null; then
        error "API não está respondendo. Logs:"
        docker-compose logs browser-use-api
    fi
}

# Mostrar informações pós-deploy
show_info() {
    log "Deploy concluído com sucesso! 🎉"
    echo
    echo -e "${BLUE}📋 Informações do Deploy:${NC}"
    echo -e "  🌐 API URL: http://localhost:5000"
    echo -e "  ❤️  Health Check: http://localhost:5000/health"
    echo -e "  📚 Documentação: README.md"
    echo
    echo -e "${BLUE}🔧 Comandos úteis:${NC}"
    echo -e "  📊 Ver logs: docker-compose logs -f"
    echo -e "  🔄 Restart: docker-compose restart"
    echo -e "  🛑 Parar: docker-compose down"
    echo -e "  🗑️  Limpar: docker-compose down -v --rmi all"
    echo
    echo -e "${BLUE}🧪 Testar API:${NC}"
    echo -e "  curl -X GET http://localhost:5000/health"
    echo -e "  python test_api.py"
    echo
}

# Menu principal
show_menu() {
    echo -e "${BLUE}🚀 Browser Use API - Script de Deploy${NC}"
    echo
    echo "Escolha o tipo de deploy:"
    echo "1) Básico (apenas API)"
    echo "2) Com Nginx (API + Proxy Reverso)"
    echo "3) Completo (API + Nginx + Redis)"
    echo "4) Verificar status"
    echo "5) Ver logs"
    echo "6) Parar serviços"
    echo "7) Sair"
    echo
}

# Função principal
main() {
    log "Iniciando script de deploy..."
    
    # Verificações iniciais
    check_docker
    check_env
    
    # Se argumento foi passado, usar diretamente
    if [ $# -eq 1 ]; then
        case $1 in
            "basic"|"1")
                build_app
                deploy_basic
                check_status
                show_info
                ;;
            "nginx"|"2")
                build_app
                deploy_with_nginx
                check_status
                show_info
                ;;
            "full"|"3")
                build_app
                deploy_full
                check_status
                show_info
                ;;
            *)
                error "Argumento inválido. Use: basic, nginx, ou full"
                ;;
        esac
        return
    fi
    
    # Menu interativo
    while true; do
        show_menu
        read -p "Escolha uma opção (1-7): " choice
        
        case $choice in
            1)
                build_app
                deploy_basic
                check_status
                show_info
                break
                ;;
            2)
                build_app
                deploy_with_nginx
                check_status
                show_info
                break
                ;;
            3)
                build_app
                deploy_full
                check_status
                show_info
                break
                ;;
            4)
                docker-compose ps
                ;;
            5)
                docker-compose logs -f
                ;;
            6)
                log "Parando serviços..."
                docker-compose down
                log "Serviços parados ✓"
                ;;
            7)
                log "Saindo..."
                exit 0
                ;;
            *)
                warn "Opção inválida. Tente novamente."
                ;;
        esac
    done
}

# Executar função principal
main "$@"
