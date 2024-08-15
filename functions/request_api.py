import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from Models.model import APIError
from config.config import TIMOUT
from config.log_config import logger
from functions.get_headers import get_headers
import xml.etree.ElementTree as ET

timeout=TIMOUT

def make_request(method: str, url: str, **kwargs) -> tuple:
    headers = get_headers()
    
    # Always set Content-Type to XML
    headers['Content-Type'] = 'application/xml'
    
    logger.debug(f"Making {method} request to {url} with headers: {headers}")

    try:
        response = requests.request(method, url, headers=headers, verify=False, timeout=timeout, **kwargs)

        # Log the full response
        logger.debug(f"Received response [{response.status_code}] from {url}")
        logger.debug(f"Response content: {response.text}")

        result = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.text,
            'xml': None
        }

        if response.status_code != 404:
            response.raise_for_status()

            try:
                xml_content = ET.fromstring(response.text)
                result['xml'] = xml_content
            except ET.ParseError as e:
                logger.error(f"Failed to parse XML response: {e}")

        return response.status_code, result

    except HTTPError as http_err:
        if response.status_code != 404:
            error = APIError(f"HTTP error occurred: {http_err}")
            error.status_code = response.status_code
            error.response_content = response.text
            error.response_headers = dict(response.headers)
            logger.error(f"HTTP Error: {error.message} with Status Code: {error.status_code}")
            raise error
        else:
            return 404, {
                'status_code': 404,
                'headers': dict(response.headers),
                'content': response.text,
                'xml': None
            }


    except ConnectionError as conn_err:
        error = APIError(f"Connection error occurred: {conn_err}")
        logger.error(error.message)
        raise error

    except Timeout as timeout_err:
        error = APIError(f"Timeout error occurred: {timeout_err}")
        logger.error(error.message)
        raise error

    except RequestException as req_err:
        error = APIError(f"An error occurred while making the request: {req_err}")
        logger.error(error.message)
        raise error

    except Exception as e:
        error = APIError(f"An unexpected error occurred: {e}")
        logger.error(error.message)
        raise error