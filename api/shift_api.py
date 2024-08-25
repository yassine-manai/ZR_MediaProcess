from typing import Tuple
from config.config import CASHIER_CONSUMER_ID, CASHIER_CONTRACT_ID, COMPUTER_ID, DEVICE_ID, ZR_IP, ZR_PORT
from functions.check_error import handle_api_error
from functions.request_api import make_request
from config.log_config import logger
from globals.global_vars import configuration_data


class ShiftPaymentAPIClient:
    def __init__(self):
        global configuration_data

        # Configuration data or default values
        self.ip_url = configuration_data.get("zr_ip", ZR_IP)
        self.port = configuration_data.get("zr_port", ZR_PORT)
        self.username = configuration_data.get("zr_username", "default_user")
        self.password = configuration_data.get("zr_password", "default_password")
        
        self.computer_id = configuration_data.get("computer_id", COMPUTER_ID)
        self.device_id = configuration_data.get("device_id", DEVICE_ID)
        self.cashier_contract_id = configuration_data.get("cashier_contract_id", CASHIER_CONTRACT_ID)
        self.cashier_consumer_id = configuration_data.get("cashier_consumer_id", CASHIER_CONSUMER_ID)
        
        
        self.url = f"{self.ip_url}:{self.port}"
        self.protocol = "https"
        self.url_api_shift = f"{self.protocol}://{self.url}/PaymentWebService"

    # Shift Section

    @handle_api_error
    def open_shift_api(self, data: str) -> Tuple[int, dict]:
        return make_request("POST", f"{self.url_api_shift}/shifts", data=data)

    @handle_api_error
    def get_current_shift_api(self, shift_status: int) -> Tuple[int, dict]:
        logger.debug("GET OPEN SHIFT ....")
        return make_request(
            "GET", 
            f"{self.url_api_shift}/cashiers/{self.cashier_contract_id},{self.cashier_consumer_id}/shifts?shiftStatus={shift_status}&deviceId={self.device_id}"
        )

    @handle_api_error
    def close_shift_api(self, shift_id: int, data: str) -> Tuple[int, dict]:
        logger.debug("Closing SHIFT ....")
        return make_request("PUT", f"{self.url_api_shift}/shifts/{shift_id}", data=data)

    # Payment Section

    @handle_api_error
    def topup_pmvc_api(self, shift_id: int, data: str) -> Tuple[int, dict]:
        logger.debug("TOPUP_PMVC in progress ....")
        return make_request("PUT", f"{self.url_api_shift}/shifts/{shift_id}/salestransactions", data=data)

