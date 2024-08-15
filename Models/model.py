
from typing import Any


class APIError(Exception):
    message: str = ""
    status_code: int = None
    response_content: Any = None
    
    
