from api.shift_api import get_current_shift, open_shift, close_shift, topup_pmvc_api
from functions.shift_dict_xml import topup_pmvc_xml
from functions.xml_resp_parser import current_shift_response, open_shift_response
from config.log_config import logger

def shift_ptcpt(data_topup, data_open, data_close):
        
    # -------------------------------------- Check existance ----------------------------------------------------------
    status_code, shift_deatil = get_current_shift()
    
    # -------------------------------------- if shift exist ----------------------------------------------------------
    if status_code == 200: 
        # Get Shift deatail 
        shift_status, shift_id, shift_no = current_shift_response(shift_deatil)
        logger.debug(f"SHIFT Status : {shift_status} -- SHIFT ID :{shift_id} -- SHIFT NB :{shift_no}")
        
        # topup pmvc
        data_topup_xml = topup_pmvc_xml()
        status_code, shift_deatil = topup_pmvc_api(shift_id, data_topup)
        
        if status_code == 200:
            logger.info(f"Topup PMVC for Shift ID {shift_id} successful")
            logger.debug(f"Response {status_code} from Shift {shift_deatil}")

            #Close SHIFT
            status_code, shift_deatil = close_shift(shift_id, data_topup)

            if status_code == 200:
                logger.info(f"Close Shift for Shift ID {shift_id} successful")
                logger.debug(f"Response {status_code} from Shift {shift_deatil}")
                
            if status_code != 200:
                logger.error(f"Error Occured while closing Shift ID {shift_id}")
                logger.debug(f"Response {status_code} Sfrom Shift {shift_deatil}")
        
        if status_code != 200:
            logger.error(f"Error Occured while TOPUP {shift_id}")
            logger.debug(f"Response {status_code} from Shift {shift_deatil}")




    # -------------------------------------- if shift not exist ----------------------------------------------------------
    if status_code == 400:
        status_code, shift_deatil = open_shift(data_open)
        shift_status, shift_id, shift_no = open_shift_response(shift_deatil)
        
        if status_code == 200:
            logger.info(f"Shift {shift_id} Opened successful")
            logger.debug(f"Response {status_code} from Shift {shift_deatil}")

            #Close SHIFT
            status_code, shift_deatil = close_shift(shift_id, data_topup)

            if status_code == 200:
                logger.info(f"Close Shift for Shift ID {shift_id} successful")
                logger.debug(f"Response {status_code} from Shift {shift_deatil}")
                
            if status_code != 200:
                logger.error(f"Error Occured while closing Shift ID {shift_id}")
                logger.debug(f"Response {status_code} Sfrom Shift {shift_deatil}")
        
        if status_code != 200:
            logger.error(f"Error Occured while closing Shift ID {shift_id}")
            logger.debug(f"Response {status_code} from Shift {shift_deatil}")
