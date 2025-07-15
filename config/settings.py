import os
import getpass
from datetime import datetime

# Get the absolute path to this file (settings.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Base directory is one level up from config/
BASE_DIR = os.path.dirname(current_dir)

# Data directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')
PORTFOLIOS_DIR = os.path.join(DATA_DIR, 'portfolios')
REPORTS_DIR = os.path.join(DATA_DIR, 'reports')

# Create directories if not exists
for d in [DATA_DIR, LOGS_DIR, PORTFOLIOS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Current user and timestamp
CURRENT_USER = getpass.getuser()
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# Path to logging configuration
LOGGING_CONF = os.path.join(current_dir, 'logging.conf')
