import logging
import os
import json
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Create logs directory if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log file format (logs_YYYYMMDD.log)
LOG_FILENAME = os.path.join(LOG_DIR, f"logs_{datetime.now().strftime('%Y%m%d')}.log")

# Setup log handler for daily rotation at midnight
handler = TimedRotatingFileHandler(
    LOG_FILENAME, when="midnight", interval=1, backupCount=30, encoding="utf-8"
)
handler.suffix = "%Y%m%d"  # Ensures the filename changes every day at midnight

# Log format
log_format = "%(asctime)s - %(levelname)s - %(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)

# Create logger
logger = logging.getLogger("ecommerce_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Suppress passlib warnings
logging.getLogger("passlib").setLevel(logging.ERROR)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all requests and responses"""

    async def dispatch(self, request: Request, call_next):
        """Intercepts request and response for logging"""
        try:
            body = await request.body()
            masked_body = mask_sensitive_data(body.decode("utf-8"))

            # Log request details
            logger.info(
                f"Request: {request.method} {request.url} | Headers: {dict(request.headers)} | Body: {masked_body}"
            )

            response = await call_next(request)
            response_body = [section async for section in response.body_iterator]
            response.body_iterator = iter(response_body)

            # Log response details
            response_text = b"".join(response_body).decode("utf-8")
            masked_response = mask_sensitive_data(response_text)
            logger.info(
                f"Response: {response.status_code} | Headers: {dict(response.headers)} | Body: {masked_response}"
            )

            return Response(content=b"".join(response_body), status_code=response.status_code, headers=dict(response.headers))
        except Exception as e:
            logger.error(f"LoggingMiddleware Error: {str(e)}")
            return await call_next(request)

def mask_sensitive_data(data):
    """Replace sensitive fields like passwords or tokens with '******'"""
    try:
        json_data = json.loads(data)
        if isinstance(json_data, dict):
            if "password" in json_data:
                json_data["password"] = "******"
            if "token" in json_data:
                json_data["token"] = "******"
        return json.dumps(json_data)
    except json.JSONDecodeError:
        return data  # If data is not JSON, return as-is

