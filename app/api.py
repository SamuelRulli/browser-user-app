from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import time
import requests
from typing import Dict, Any, Optional, List
import os

app = Flask(__name__)
CORS(app)

# Configurações da API Browser Use
API_KEY = os.getenv('BROWSER_USE_API_KEY', 'bu_qmQQk3-mrRbXvhq9kNurpAxQXvwF0meWyU6e8GvAxu0')
BASE_URL = 'https://api.browser-use.com/api/v1'
HEADERS = {'Authorization': f'Bearer {API_KEY}'}


class BrowserUseAPI:
    """Cliente para interagir com a API Browser Use"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or API_KEY
        self.headers = {'Authorization': f'Bearer {self.api_key}'}
    
    def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executa uma nova task"""
        response = requests.post(f'{BASE_URL}/run-task', headers=self.headers, json=task_data)
        response.raise_for_status()
        return response.json()
    
    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Obtém detalhes completos da task"""
        response = requests.get(f'{BASE_URL}/task/{task_id}', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Obtém apenas o status da task"""
        response = requests.get(f'{BASE_URL}/task/{task_id}/status', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def stop_task(self, task_id: str) -> Dict[str, Any]:
        """Para uma task em execução"""
        response = requests.put(f'{BASE_URL}/task/{task_id}/stop', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def pause_task(self, task_id: str) -> Dict[str, Any]:
        """Pausa uma task em execução"""
        response = requests.put(f'{BASE_URL}/task/{task_id}/pause', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def resume_task(self, task_id: str) -> Dict[str, Any]:
        """Resume uma task pausada"""
        response = requests.put(f'{BASE_URL}/task/{task_id}/resume', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def list_tasks(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """Lista todas as tasks"""
        params = {'limit': limit, 'offset': offset}
        response = requests.get(f'{BASE_URL}/tasks', headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_task_media(self, task_id: str) -> Dict[str, Any]:
        """Obtém mídia da task"""
        response = requests.get(f'{BASE_URL}/task/{task_id}/media', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_task_screenshots(self, task_id: str) -> Dict[str, Any]:
        """Obtém screenshots da task"""
        response = requests.get(f'{BASE_URL}/task/{task_id}/screenshots', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_task_gif(self, task_id: str) -> Dict[str, Any]:
        """Obtém GIF da task"""
        response = requests.get(f'{BASE_URL}/task/{task_id}/gif', headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, task_id: str, poll_interval: int = 2, timeout: int = 300) -> Dict[str, Any]:
        """Aguarda a conclusão da task com timeout"""
        start_time = time.time()
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Task {task_id} não foi concluída em {timeout} segundos")
            
            task_details = self.get_task(task_id)
            status = task_details['status']
            
            if status in ['finished', 'failed', 'stopped']:
                return task_details
            
            time.sleep(poll_interval)


# Instância global do cliente
browser_api = BrowserUseAPI()


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'service': 'browser-use-api'
    })


@app.route('/api/v1/run-task', methods=['POST'])
def run_task():
    """
    Executa uma nova task de automação do browser
    
    Body esperado:
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
    """
    try:
        data = request.get_json()
        
        if not data or 'task' not in data:
            return jsonify({'error': 'Campo "task" é obrigatório'}), 400
        
        # Extrai parâmetros específicos da nossa API
        wait_for_completion = data.pop('wait_for_completion', False)
        timeout = data.pop('timeout', 300)
        
        # Executa a task
        result = browser_api.run_task(data)
        task_id = result['id']
        
        if wait_for_completion:
            # Aguarda conclusão e retorna resultado completo
            try:
                final_result = browser_api.wait_for_completion(task_id, timeout=timeout)
                return jsonify({
                    'task_id': task_id,
                    'status': 'completed',
                    'result': final_result
                })
            except TimeoutError as e:
                return jsonify({
                    'task_id': task_id,
                    'status': 'timeout',
                    'error': str(e),
                    'partial_result': browser_api.get_task(task_id)
                }), 408
        else:
            # Retorna apenas o ID da task
            return jsonify({
                'task_id': task_id,
                'status': 'created',
                'message': 'Task criada com sucesso. Use /api/v1/task/{task_id} para acompanhar o progresso.'
            })
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>', methods=['GET'])
def get_task(task_id: str):
    """Obtém detalhes completos da task"""
    try:
        result = browser_api.get_task(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/status', methods=['GET'])
def get_task_status(task_id: str):
    """Obtém apenas o status da task"""
    try:
        result = browser_api.get_task_status(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/stop', methods=['PUT'])
def stop_task(task_id: str):
    """Para uma task em execução"""
    try:
        result = browser_api.stop_task(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/pause', methods=['PUT'])
def pause_task(task_id: str):
    """Pausa uma task em execução"""
    try:
        result = browser_api.pause_task(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/resume', methods=['PUT'])
def resume_task(task_id: str):
    """Resume uma task pausada"""
    try:
        result = browser_api.resume_task(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/tasks', methods=['GET'])
def list_tasks():
    """Lista todas as tasks"""
    try:
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        result = browser_api.list_tasks(limit=limit, offset=offset)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/media', methods=['GET'])
def get_task_media(task_id: str):
    """Obtém mídia da task"""
    try:
        result = browser_api.get_task_media(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/screenshots', methods=['GET'])
def get_task_screenshots(task_id: str):
    """Obtém screenshots da task"""
    try:
        result = browser_api.get_task_screenshots(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/gif', methods=['GET'])
def get_task_gif(task_id: str):
    """Obtém GIF da task"""
    try:
        result = browser_api.get_task_gif(task_id)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.route('/api/v1/task/<task_id>/wait', methods=['GET'])
def wait_for_task_completion(task_id: str):
    """Aguarda a conclusão de uma task específica"""
    try:
        timeout = request.args.get('timeout', 300, type=int)
        poll_interval = request.args.get('poll_interval', 2, type=int)
        
        result = browser_api.wait_for_completion(task_id, poll_interval=poll_interval, timeout=timeout)
        return jsonify({
            'task_id': task_id,
            'status': 'completed',
            'result': result
        })
    except TimeoutError as e:
        return jsonify({
            'task_id': task_id,
            'status': 'timeout',
            'error': str(e),
            'partial_result': browser_api.get_task(task_id)
        }), 408
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Erro na API Browser Use: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método não permitido'}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 9000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
