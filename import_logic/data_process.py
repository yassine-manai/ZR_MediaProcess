""" from api.api_media import create_company, create_participant, get_company_details, get_participant
from functions.dict_xml import consumer_to_xml, contract_to_xml
from functions.xml_resp_parser import company_reponse_parser, participant_response_parser
from globals.global_vars import glob_vals
from config.log_config import logger


def company_process(mylistc) -> bool:
    company_name_id_map = {}

    for rowc in mylistc:
        company_id = rowc.get('Company_id')
        company_name = rowc.get('Company_Name')

        if company_name in company_name_id_map:
            existing_id = company_name_id_map[company_name]
            if existing_id != company_id:
                logger.warning(f"Duplicate company name '{company_name}' found with different IDs: "
                            f"{existing_id} (existing) and {company_id} (new).")
                continue

        status_code, company_details = get_company_details(company_id)

        # Company found
        if status_code != 404:
            logger.info(f"Company ID {company_id} found in the list of companies")
            logger.debug(company_details)

            id, name, _, _, _ = company_reponse_parser(company_details)
            logger.debug(f"id: {id}")
            logger.debug(f"name: {name}")

            # Add the company name and ID to the map if it doesn't exist yet
            company_name_id_map[company_name] = company_id


        # Company not found
        if status_code == 404:
            logger.info(f"Company ID {company_id} not found")
            try:
                xml_comp_data = contract_to_xml(rowc)
                status_code, result = create_company(xml_comp_data)
                logger.debug(f"Status code: {status_code}")
                logger.debug(result)

                if status_code == 201:
                    logger.info(f"Company ID {company_id} created successfully --------------- ")
                    # Add the new company name and ID to the map
                    company_name_id_map[company_name] = company_id
                else:
                    logger.error(f"Failed to create Company ID {company_id}. Status code: {status_code}")
            except Exception as e:
                logger.error(f"Error creating Company {company_id}: {e}")
                
                
                
                
def participant_process(mylistp):
    for rowp in mylistp:
        global glob_vals
        template_ids = glob_vals

        participant_id = rowp.get('Participant_Id')
        company_id = rowp.get('Company_id')
        
        status_code, participant_details = get_participant(company_id, participant_id)

        #participant found 
        if status_code != 404:
            logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                            
            #ptcpt_id, contractid,name, surname, _, _, _ = participant_response_parser(participant_details)
            #logger.debug(f"Participant {name} {surname} with id: {ptcpt_id} -- Commpany Associated : {contractid}")
            #logger.debug(f"Participant {name} {surname} with id: {ptcpt_id} -- Commpany Associated : {contractid}")

        # participant not found   
        if status_code == 404:
            logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")

            ptcpt_type = rowp.get('Participant_Type', 3)
            if ptcpt_type == 2:
                template_id = template_ids["season_parker"]
            if ptcpt_type == 6:
                template_id = template_ids["pmvc"]
            if ptcpt_type == 6:
                template_id = template_ids["cmp"]
                
                
            xml_ptcpt_data = consumer_to_xml(rowp)     
            logger.debug(xml_ptcpt_data) 
                           
            status_code, result = create_participant(company_id, 3, xml_ptcpt_data)
                                        
            logger.info(f"Status code: {status_code}")
            logger.debug(f"Status code: {status_code}")
            logger.debug(result)
            print("\n")
            
            
            if status_code == 201:
                logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                
            if status_code == 500:
                logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")
 """