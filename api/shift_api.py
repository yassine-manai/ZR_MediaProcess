from typing import Tuple
from config.config import CASHIER_CONSUMER_ID, CASHIER_CONTRACT_ID, DEVICE_ID
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

url_api_shift = f"https://{ip_fix}/PaymentWebService"



#  ---------------------------------------------------------- SHIFT Section -------------------------------------------------------------------

# OPEN SHIFT
@handle_api_error
def open_shift_api(data: str) -> Tuple[int, dict]:
    return make_request("POST", f"{url_api_shift}/shifts", data=data)

#GET CURRENT SHIFT
@handle_api_error
def get_current_shift_api(shft_status: int) -> Tuple[int, dict]:
    logger.debug(f"GET OPEN SHIFT ....")
    return make_request("GET", f"{url_api_shift}/cashiers/{CASHIER_CONTRACT_ID},{CASHIER_CONSUMER_ID}/shifts?shiftStatus={shft_status}&deviceId={DEVICE_ID}")


#CLOSE SHIFT
@handle_api_error
def close_shift_api(shift_id: int, data: str) -> Tuple[int, dict]:
    logger.debug(f"GET OPEN SHIFT ....")
    return make_request("GET", f"{url_api_shift}/shifts/{shift_id}", data=data)



#  ---------------------------------------------------------- PAYMENT Section -------------------------------------------------------------------

#TOP-UP PMVC
@handle_api_error
def topup_pmvc_api(shift_id: int, data: str) -> Tuple[int, dict]:
    logger.debug(f"TOPUP_PMVC in progress ....")
    return make_request("PUT", f"{url_api_shift}/shifts/{shift_id}/salestransactions", data=data)
