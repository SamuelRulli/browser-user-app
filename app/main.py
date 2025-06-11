import json
import time
import os

import requests

# Importar configurações
from .config import Config

HEADERS = Config.get_headers()


def create_task(instructions: str):
	"""Create a new browser automation task"""
	response = requests.post(f'{Config.BROWSER_USE_BASE_URL}/run-task', headers=HEADERS, json={'task': instructions})
	return response.json()['id']


def get_task_status(task_id: str):
	"""Get current task status"""
	response = requests.get(f'{Config.BROWSER_USE_BASE_URL}/task/{task_id}/status', headers=HEADERS)
	return response.json()


def get_task_details(task_id: str):
	"""Get full task details including output"""
	response = requests.get(f'{Config.BROWSER_USE_BASE_URL}/task/{task_id}', headers=HEADERS)
	return response.json()


def wait_for_completion(task_id: str, poll_interval: int = None):
	"""Poll task status until completion"""
	# Usar valor padrão da configuração se não fornecido
	if poll_interval is None:
		poll_interval = Config.DEFAULT_POLL_INTERVAL
		
	count = 0
	unique_steps = []
	while True:
		details = get_task_details(task_id)
		new_steps = details['steps']
		# use only the new steps that are not in unique_steps.
		if new_steps != unique_steps:
			for step in new_steps:
				if step not in unique_steps:
					print(json.dumps(step, indent=4))
			unique_steps = new_steps
		count += 1
		status = details['status']

		if status in ['finished', 'failed', 'stopped']:
			return details
		time.sleep(poll_interval)


def main():
	task_id = create_task('Open https://www.google.com and search for openai')
	print(f'Task created with ID: {task_id}')
	task_details = wait_for_completion(task_id)
	print(f"Final output: {task_details['output']}")


if __name__ == '__main__':
	main()
