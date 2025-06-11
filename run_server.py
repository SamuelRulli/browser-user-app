#!/usr/bin/env python3
"""
Script para iniciar o servidor da API
"""

import os
import sys
from app.api import app

if __name__ == '__main__':
    port = int(os.getenv('PORT', 9000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Iniciando API Browser Use Wrapper na porta {port}")
    print(f"📍 URL: http://localhost:{port}")
    print(f"🔧 Debug mode: {debug}")
    print("📋 Endpoints disponíveis:")
    print("   GET  /health")
    print("   POST /api/v1/run-task")
    print("   GET  /api/v1/task/{task_id}")
    print("   GET  /api/v1/task/{task_id}/status")
    print("   ... e mais (veja README.md)")
    print("\n✋ Pressione Ctrl+C para parar o servidor\n")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Servidor parado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
