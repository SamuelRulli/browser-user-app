"""
Configurações da aplicação Browser Use API
"""
import os
from typing import Optional

def load_env_file(env_file: str = '.env') -> None:
    """
    Carrega variáveis de ambiente de um arquivo .env
    """
    if not os.path.exists(env_file):
        return
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key and not os.getenv(key):
                    os.environ[key] = value

# Carregar arquivo .env se existir
load_env_file()

class Config:
    """Configurações da aplicação"""
    
    # API Browser Use
    BROWSER_USE_API_KEY: Optional[str] = os.getenv('BROWSER_USE_API_KEY')
    BROWSER_USE_BASE_URL: str = os.getenv('BROWSER_USE_BASE_URL', 'https://api.browser-use.com/api/v1')
    
    # Flask
    PORT: int = int(os.getenv('PORT', 5000))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Timeouts e intervalos
    DEFAULT_TIMEOUT: int = int(os.getenv('DEFAULT_TIMEOUT', 300))
    DEFAULT_POLL_INTERVAL: int = int(os.getenv('DEFAULT_POLL_INTERVAL', 2))
    
    @classmethod
    def validate(cls) -> None:
        """Valida se todas as configurações obrigatórias estão presentes"""
        if not cls.BROWSER_USE_API_KEY:
            raise ValueError(
                "BROWSER_USE_API_KEY não está configurada. "
                "Configure a variável de ambiente ou crie um arquivo .env"
            )
    
    @classmethod
    def get_headers(cls) -> dict:
        """Retorna headers para requisições à API Browser Use"""
        return {'Authorization': f'Bearer {cls.BROWSER_USE_API_KEY}'}

# Validar configurações na importação
Config.validate()
