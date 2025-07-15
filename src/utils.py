import os
import sys

def get_project_root():
    """Get the absolute path to the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(current_dir))

def add_project_root_to_path():
    """Add project root to Python path for module resolution"""
    project_root = get_project_root()
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
