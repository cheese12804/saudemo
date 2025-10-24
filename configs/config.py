import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_config(env_var: str):
    return os.getenv(f"_{env_var}") if os.getenv(f"_{env_var}") else os.getenv(env_var)

def open_json(file_path: str):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    full_path = os.path.join(project_root, file_path)
    with open(full_path, encoding="utf-8") as f:
        return json.load(f)
def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def get_absolute_path(relative_path: str):
    return os.path.join(get_project_root(), relative_path)
class Config:
    LOGIN_URL = open_json("utils/url.json")["BASE_URL"]
    BROWSER = get_config("BROWSER")
    IMPLICIT_WAIT = int(get_config("IMPLICIT_WAIT"))
    EXPLICIT_WAIT = int(get_config("EXPLICIT_WAIT"))
    LOG_FILE = get_config("LOG_FILE")
    LOG_LEVEL = get_config("LOG_LEVEL") 
