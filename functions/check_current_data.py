from api.api_media import get_company_details, get_participant
from config.log_config import logger

def check_company(company_id: int) -> bool:
    logger.info(f"Checking company with ID {company_id}")
    
    if get_company_details(company_id):
        logger.info(f"Company with ID {company_id} is found")
        return True
    else:
        logger.error(f"Company with ID {company_id} is not found")
        return False


def check_participant(company_id: int, participant_id: int) -> bool:
    logger.info(f"Checking participant with ID {participant_id} for company {company_id}")
    
    if get_participant(company_id, participant_id):
        logger.info(f"Participant with ID {participant_id} is found for company {company_id}")
        return True
    else:
        logger.error(f"Participant with ID {participant_id} is not found for company {company_id}")
        return False
    