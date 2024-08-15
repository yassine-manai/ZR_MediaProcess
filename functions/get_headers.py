from typing import Dict
from globals.global_vars import token_data


def get_headers() -> Dict[str, str]:

    global token_data
    token = token_data.get("access_token")

    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/xml"
    }