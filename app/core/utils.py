# app\core\utils.py

import logging
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Bangkok')

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ecommerce-api")

def log_request(request):
    logger.info(f"Request: {request.method} {request.url}")

def log_response(response):
    logger.info(f"Response: {response.status_code}")
