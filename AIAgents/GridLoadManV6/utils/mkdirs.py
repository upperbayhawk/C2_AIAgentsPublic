from pathlib import Path

# Define the base project directory
project_root = Path('C:\C2_AIAgents\AIAgents\GridLoadManGEN5\AgentWorld')

# Define the directory structure
directories = [
    project_root / 'agents' / 'main_agent',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_1',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_2',
    project_root / 'agents' / 'workers' / 'worker_1',
    project_root / 'agents' / 'workers' / 'worker_2',
    project_root / 'core',
    project_root / 'config',
    project_root / 'logs',
    project_root / 'tests'
]

# Create the directories
for directory in directories:
    directory.mkdir(parents=True, exist_ok=True)
    print(f'Created directory: {directory}')

# Create placeholder files
files = [
    project_root / 'agents' / 'main_agent' / '__init__.py',
    project_root / 'agents' / 'main_agent' / 'main_agent.py',
    project_root / 'agents' / 'main_agent' / 'config.yaml',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_1' / '__init__.py',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_1' / 'assistant_agent_1.py',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_1' / 'config.yaml',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_2' / '__init__.py',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_2' / 'assistant_agent_2.py',
    project_root / 'agents' / 'assistant_agents' / 'assistant_agent_2' / 'config.yaml',
    project_root / 'agents' / 'workers' / 'worker_1' / '__init__.py',
    project_root / 'agents' / 'workers' / 'worker_1' / 'worker_1.py',
    project_root / 'agents' / 'workers' / 'worker_1' / 'config.yaml',
    project_root / 'agents' / 'workers' / 'worker_2' / '__init__.py',
    project_root / 'agents' / 'workers' / 'worker_2' / 'worker_2.py',
    project_root / 'agents' / 'workers' / 'worker_2' / 'config.yaml',
    project_root / 'core' / '__init__.py',
    project_root / 'core' / 'task_manager.py',
    project_root / 'core' / 'communication.py',
    project_root / 'core' / 'data_processing.py',
    project_root / 'config' / 'settings.yaml',
    project_root / 'tests' / 'test_main_agent.py',
    project_root / 'tests' / 'test_assistant_agent_1.py',
    project_root / 'tests' / 'test_worker_1.py',
    project_root / 'requirements.txt',
    project_root / 'README.md'
]

# Create the files
for file in files:
    file.touch(exist_ok=True)
    print(f'Created file: {file}')
