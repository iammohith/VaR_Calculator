import os
import sys

def get_project_root():
    """Get the absolute path to the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
