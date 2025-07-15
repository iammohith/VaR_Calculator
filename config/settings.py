import os
import getpass
from datetime import datetime

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, 'data')
LOGS_DIR = os.path.join(DATA_DIR, 'logs')
PORTFOLIOS_DIR = os.path.join(DATA_DIR, 'portfolios')
RESULTS_DIR = os.path.join(DATA_DIR, 'results')
REPORTS_DIR = os.path.join(DATA_DIR, 'reports')

# Create directories if not exists
for d in [LOGS_DIR, PORTFOLIOS_DIR, RESULTS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

# Current user and timestamp
CURRENT_USER = getpass.getuser()
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
