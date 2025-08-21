import os
import sys
import logging

# Set up logging
logging_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Use absolute path for logs directory (relative to this file)
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'my_project.log')

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.info("Initializing my_project package")

__version__ = "0.1.0"