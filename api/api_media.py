from typing import Tuple
from functions.check_error import handle_api_error
from functions.request_api import make_request
from config.log_config import logger
from globals.global_vars import zr_data


#https://193.95.82.173:8709/CustomerMediaWebService/contracts
ip_fix = "193.95.82.173:8709"


ip_url = zr_data.get("zr_ip")
port = zr_data.get("zr_port")
username = zr_data.get("username")
password = zr_data.get("password")


url_api = f"https://{ip_fix}/CustomerMediaWebService"
#logger.debug(url_api)

# Company Section
@handle_api_error
def get_company_details(company_id: int) -> Tuple[int, dict]:
    return make_request("GET", f"{url_api}/contracts/{company_id}/detail")

@handle_api_error
def create_company(data: str) -> Tuple[int, dict]:
    logger.debug(f"Creating company with data: {data}")
    return make_request("POST", f"{url_api}/contracts", data=data)



# Participant Part
@handle_api_error
def create_participant(company_id: int, template_id: int, data: str) -> Tuple[int, dict]:
    logger.debug(f"Creating participant for company ID {company_id} with template ID {template_id}")
    return make_request("POST", f"{url_api}/contracts/{company_id}/consumers?templateId={template_id}", data=data)

@handle_api_error
def get_participant(company_id: int, participant_id: int) -> Tuple[int, dict]:
    return make_request("GET", f"{url_api}/consumers/{company_id},{participant_id}")



# PUT METHs 
@handle_api_error
def Update_participant(company_id: int, participant_id: int, data: str) -> Tuple[int, dict]:
    logger.debug(f"Upddating participant for company ID {company_id}  -- to {data}")
    return make_request("PUT", f"{url_api}/consumers/{company_id},{participant_id}/detail", data=data)


@handle_api_error
def Update_company(company_id: int, data: str) -> Tuple[int, dict]:
    logger.debug(f"Upddating company {company_id}  ------ to {data}")
    return make_request("PUT", f"{url_api}/contracts/{company_id}/detail", data=data)




# ZR GET VERSION
@handle_api_error
def get_company_version() -> Tuple[int, dict]:
    return make_request("GET", f"{url_api}/version")
