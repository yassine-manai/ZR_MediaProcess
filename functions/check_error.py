import requests
from typing import Any, Optional
from config.log_config import logger

class Error(Exception):

    def __init__(self, message: str, status_code: Optional[int] = None, response_content: Any = None):
        
        self.message = message
        self.status_code = status_code
        self.response_content = response_content
        super().__init__(self.message)

def handle_api_error(func):
    
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
        
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            #raise Error(f"Invalid input: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            #raise Error(f"Unexpected error: {str(e)}")
    return wrapper
