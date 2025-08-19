import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

project_name = "my_project"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/entity/config_entity.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",
    "main.py",
    "app.py",
    "dockerfile",
    "requirements.txt",
    "pyproject.toml",  # replaced setup.py with pyproject.toml
    "research/trials.ipynb",
    "templates/index.html",
    "tests.py",
]

for file_path_str in list_of_files:
    file_path = Path(file_path_str)
    dir_path = file_path.parent

    try:
        if dir_path and not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created directory: {dir_path}")

        if not file_path.exists() or file_path.stat().st_size == 0:
            file_path.touch(exist_ok=True)
            logging.info(f"Created file: {file_path}")
        else:
            logging.info(f"{file_path.name} already exists and is not empty, skipping creation.")
    except Exception as e:
        logging.error(f"Error creating {file_path}: {e}")