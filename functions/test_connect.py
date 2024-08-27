from config.log_config import logger 
from tkinter import messagebox
from api.api_media import APIClient
from globals.global_vars import configuration_data

def test_zr_connection():
    global configuration_data
    logger.info("Checking ZR connection")
    
    logger.info(f"------------ {configuration_data}")

    api_client = APIClient()
    
    try:
        status_code, version = api_client.get_company_version()
        
        if status_code != 404:
            logger.success("Connection established")
            logger.debug(f"Version Response : {version}")
            logger.debug(f"Status Code Response : {status_code}")            
            messagebox.showinfo("Success", f"ZR Connection Established successfully")
            
    
        if status_code == 404:
            logger.debug(f"Version Response : {version}")
            logger.debug(f"Status Code Response : {status_code}")
            logger.error(f"Connection not established with ZR \n")
            messagebox.showinfo("Retry", "Connection not established with ZR. \n Would you like to retry?")
            
        
        return status_code

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An error occurred while trying to establish ZR connection.")