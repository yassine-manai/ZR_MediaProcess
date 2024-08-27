from typing import Tuple
from functions.check_error import handle_api_error
from functions.request_api import make_request
from config.log_config import logger
from globals.global_vars import configuration_data


class APIClient:
    def __init__(self):
        global configuration_data

        # Use configuration data or fallback to defaults
        self.ip_url = configuration_data.get("zr_ip")
        self.port = configuration_data.get("zr_port")
        self.username = configuration_data.get("zr_username")
        self.password = configuration_data.get("zr_password")
        self.url = f"{self.ip_url}:{self.port}"
        
        self.protocol = "https"
        self.url_api = f"{self.protocol}://{self.url}/CustomerMediaWebService"

    # Company Section
    @handle_api_error
    def get_company_details(self, company_id: int) -> Tuple[int, dict]:
        return make_request("GET", f"{self.url_api}/contracts/{company_id}/detail")

    @handle_api_error
    def create_company(self, data: str) -> Tuple[int, dict]:
        logger.debug(f"Creating company with data: {data}")
        return make_request("POST", f"{self.url_api}/contracts", data=data)

    # Participant Section
    @handle_api_error
    def create_participant(self, company_id: int, template_id: int, data: str) -> Tuple[int, dict]:
        logger.debug(f"Creating participant for company ID {company_id} with template ID {template_id} ++++++++ {data}")
        return make_request("POST", f"{self.url_api}/contracts/{company_id}/consumers?templateId={template_id}", data=data)

    @handle_api_error
    def get_participant(self, company_id: int, participant_id: int) -> Tuple[int, dict]:
        return make_request("GET", f"{self.url_api}/consumers/{company_id},{participant_id}")

    # PUT Methods
    @handle_api_error
    def update_participant(self, company_id: int, participant_id: int, data: str) -> Tuple[int, dict]:
        logger.debug(f"Updating participant for company ID {company_id} with data: {data}")
        return make_request("PUT", f"{self.url_api}/consumers/{company_id},{participant_id}/detail", data=data)

    @handle_api_error
    def update_company(self, company_id: int, data: str) -> Tuple[int, dict]:
        logger.debug(f"Updating company {company_id} with data: {data}")
        return make_request("PUT", f"{self.url_api}/contracts/{company_id}/detail", data=data)

    # ZR GET VERSION
    @handle_api_error
    def get_company_version(self) -> Tuple[int, dict]:
        logger.debug(f"Retrieving company version from {self.url_api}")
        return make_request("GET", f"{self.url_api}/version")
