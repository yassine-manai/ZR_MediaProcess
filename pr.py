""" # ----------------------------------------------------------------  PROCESSING DATA COMPANY & SEND REQUESTS ----------------------------------------------------------------------------------------------
    
        
 # ----------------------------------------------------------------  PROCESSING DATA COMPANY & SEND REQUESTS ----------------------------------------------------------------------------------------------
       
        print("\n --------------------------  COMPANY's PROCESSING ---------------------------------------------------- ")
        for rowc in mylistc:
            print(rowc)
            
            company_id = rowc.get('Company_id')
            company_name = rowc.get('Company_Name')

            status_code, company_details = get_company_details(company_id)

            # Company found
            if status_code != 404:
                logger.info(f"Company ID {company_id} found in the list of companies")
                logger.debug(company_details)

                #id, name, _, _, _ = company_reponse_parser(company_details)
                #logger.debug(f"id: {id}")
                #logger.debug(f"name: {name}")


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
                    else:
                        logger.error(f"Failed to create Company ID {company_id}. Status code: {status_code}")
                except Exception as e:
                    logger.error(f"Error creating Company {company_id}: {e}")
        print("--------------------------------------------------------------------------------------------------------------- ")

# ----------------------------------------------------------------  PROCESSING DATA COMPANY & SEND REQUESTS ----------------------------------------------------------------------------------------------
        
        specific_field_names = ["Amount", "Participant_Type"]
            
        print("\n --------------------------  PARTICIPANT's PROCESSING ---------------------------------------------------- ")
        for rowp in mylistp:
            participant_id = rowp.get('Participant_Id')
            company_id = rowp.get('Company_id')
            
            

            status_code, participant_details = get_participant(company_id, participant_id)

            # Participant found 
            if status_code != 404:
                logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")

            # Participant not found   
            if status_code == 404:
                logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")

                ptcpt_type = rowp.get('Participant_Type', 3)
                if ptcpt_type == 2:
                    template_id = template_ids["season_parker"]
                elif ptcpt_type == 6:
                    template_id = template_ids["pmvc"]
                elif ptcpt_type == 3:
                    template_id = template_ids["cmp"]
                    
                print(rowp)
                xml_ptcpt_data = consumer_to_xml(rowp)
                logger.debug(xml_ptcpt_data)                
                status_code, result = create_participant(company_id, template_id, xml_ptcpt_data)
                                                
                logger.info(f"Status code: {status_code}")
                logger.debug(f"Status code: {status_code}")
                logger.debug(result)
                print("\n")
                
                if status_code == 201:
                    logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                    
                if status_code == 500:
                    logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")
        
        print("--------------------------------------------------------------------------------------------------------------- ")


        
        missing_fields = [field for field in specific_field_names if not any(f[0] == field for f in self.optional_fields)]

        if missing_fields:
            missing_fields_str = ', '.join(missing_fields)
            messagebox.showwarning("Warning", f"The field(s) '{missing_fields_str}' have not been added. \nPlease add them or uncheck the PMVC CheckBox.")
            return
        
        else:
            print("\n\n")
            print("------------------ CURRENT SHIFT --------------------------------------------------------------------------------- ")
            print("\n\n")

            curr_status_code, curr_shift_detail = get_current_shift_api(1)
            print(curr_shift_detail)
            print(type(curr_shift_detail))
            
            stat = get_status_code(curr_shift_detail)

            # If shift exists
            if stat == 200 or stat ==201:
                # Get Shift detail 
                shift_status, shift_id, shift_no = current_shift_response(curr_shift_detail)
                logger.info(f"SHIFT Status: {shift_status} -- SHIFT ID: {shift_id} -- SHIFT NO: {shift_no}")
                logger.info(f"SHIFT ID: {shift_id} already Opened")
                logger.debug(curr_shift_detail)

                print("\n --------------------------  PARTICIPANT's PROCESSING ---------------------------------------------------- ")
                for rowp in mylistp:
                    
                    print(rowp)
                    
                    participant_id = rowp.get('Participant_Id')
                    company_id = rowp.get('Company_id')
                    money_balance = rowp.get('Amount', 1)
                    
                    input()

                    status_code, participant_details = get_participant(company_id, participant_id)

                    # Participant found 
                    if status_code != 404:
                        logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                        
                        ptcpt_type = rowp.get('Participant_Type')
                        if ptcpt_type == 2:
                            template_id = template_ids["season_parker"]
                        elif ptcpt_type == 6:
                            template_id = template_ids["pmvc"]
                        elif ptcpt_type == 3:
                            template_id = template_ids["cmp"]
                                
                        print(participant_details)
                        print(company_id)                            
                        print(participant_id)
                        print(money_balance)
                        
                        input()

                        data = {
                            "articles": [
                                {
                                    "artClassRef": 0,
                                    "articleRef": 10624,
                                    "quantity": 1,
                                    "quantityExp": 0,
                                    "amount": 0,
                                    "influenceRevenue": 1,
                                    "influenceCashFlow": 1,
                                    "personalizedMoneyValueCard": {
                                        "ContractId": company_id,
                                        "ConsumerId": participant_id,
                                        "addMoneyValue": int(money_balance)
                                    }
                                }
                            ]
                        }
                        
                        if ptcpt_type == 6:
                            print(f"------------------------------------ TOPUP for USER #{participant_id} -- Company {company_id}#------------------------------------------ ")
                            
                            # Topup PMVC
                            print(data)
                            data_topup_xml = topup_pmvc_xml(shift_id, data)
                            print(data_topup_xml)
                            status_code_tp, shift_detail = topup_pmvc_api(shift_id, data_topup_xml)
                            
                            if status_code_tp == 200:
                                logger.success("TOPUP successfully")
                                logger.info("TOPUP successfully")
                                logger.debug(shift_detail)
                            
                            if status_code_tp != 201:
                                logger.error("ERROR !!!")
                                logger.debug(shift_detail)
                                
                    # Participant not found   
                    if status_code == 404:
                        logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")

                        ptcpt_type = rowp.get('Participant_Type')
                        if ptcpt_type == 2:
                            template_id = template_ids["season_parker"]
                        elif ptcpt_type == 6:
                            template_id = template_ids["pmvc"]
                        elif ptcpt_type == 3:
                            template_id = template_ids["cmp"]
                            
                        print(rowp)
                        xml_ptcpt_data = consumer_to_xml(rowp)
                        logger.debug(xml_ptcpt_data)
                        status_code, result = create_participant(company_id, template_id, xml_ptcpt_data)
                        
                        if status_code == 201:
                            logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")

                            data = {
                                "articles": [
                                    {
                                        "artClassRef": 0,
                                        "articleRef": 10624,
                                        "quantity": 1,
                                        "quantityExp": 0,
                                        "amount": 0,
                                        "influenceRevenue": 1,
                                        "influenceCashFlow": 1,
                                        "personalizedMoneyValueCard": {
                                            "ContractId": company_id,
                                            "ConsumerId": participant_id,
                                            "addMoneyValue": int(money_balance)
                                        }
                                    }
                                ]
                            }
                        
                            if ptcpt_type == 6:
                                print(f"------------------------------------ TOPUP for USER #{participant_id}#------------------------------------------ ")
                                
                                # Topup PMVC
                                data_topup_xml = topup_pmvc_xml(shift_id, data)
                                status_code_tp, shift_detail = topup_pmvc_api(shift_id, data_topup_xml)
                                
                                if status_code_tp == 201:
                                    logger.success("TOPUP successfully")
                                    logger.info("TOPUP successfully")
                                    logger.debug(shift_detail)
                                
                                if status_code_tp != 201:
                                    logger.error("ERROR !!!")
                                    logger.debug(shift_detail)
                                
                                print("--------------------------------------------------------------------------------------------------------------- ")

                        logger.info(f"Status code: {status_code}")
                        logger.debug(f"Status code: {status_code}")
                        logger.debug(result)
                        print("\n")
                        
                        if status_code == 500:
                            logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

                # Close SHIFT
                data_close = close_shift_xml(shift_id, shift_status)
                status_code, shift_detail = close_shift_api(shift_id, data_close)

                if status_code == 200:
                    logger.info(f"Close Shift for Shift ID {shift_id} successful")
                    logger.debug(f"Response {status_code} from Shift {shift_detail}")
                    
                else:
                    logger.error(f"Error Occurred while closing Shift ID {shift_id}")
                    logger.debug(f"Response {status_code} from Shift {shift_detail}")
            
            # If shift does not exist
            if stat != 200 or stat != 201:
                op_shift = open_shift_xml()
                status_code, shift_detail = open_shift_api(op_shift)
                
                if status_code == 200:
                    logger.info("Opening Shift successful")
                    logger.debug(f"Response {status_code} from Shift \n {shift_detail}")
                    
                    shift_status, shift_id, shift_no = open_shift_response(shift_detail)
                    logger.info(f"SHIFT Status: {shift_status} -- SHIFT ID: {shift_id} -- SHIFT NO: {shift_no}")

                    # Topup PMVC
                    print("\n --------------------------  PARTICIPANT's PROCESSING ---------------------------------------------------- ")
                    for rowp in mylistp:
                        print(rowp)
                        
                        participant_id = rowp.get('Participant_Id')
                        company_id = rowp.get('Company_id')
                        money_balance = rowp.get('Amount', 0)
                        
                        status_code, participant_details = get_participant(company_id, participant_id)

                        # Participant found 
                        if status_code != 404:
                            logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                                                    
                            ptcpt_type = rowp.get('Participant_Type')
                            if ptcpt_type == 2:
                                template_id = template_ids["season_parker"]
                            elif ptcpt_type == 6:
                                template_id = template_ids["pmvc"]
                            elif ptcpt_type == 3:
                                template_id = template_ids["cmp"]
                                        
                            data = {
                                "articles": [
                                    {
                                        "artClassRef": 0,
                                        "articleRef": 10624,
                                        "quantity": 1,
                                        "quantityExp": 0,
                                        "amount": 0,
                                        "influenceRevenue": 1,
                                        "influenceCashFlow": 1,
                                        "personalizedMoneyValueCard": {
                                            "ContractId": company_id,
                                            "ConsumerId": participant_id,
                                            "addMoneyValue": int(money_balance)
                                        }
                                    }
                                ]
                            }
                        
                            if ptcpt_type == 6:
                                print(f"------------------------------------ TOPUP for USER #{participant_id}#------------------------------------------ ")
                                
                                # Topup PMVC
                                data_topup_xml = topup_pmvc_xml(shift_id, data)
                                status_code_tp, shift_detail = topup_pmvc_api(shift_id, data_topup_xml)
                                
                                if status_code_tp == 200:
                                    logger.success("TOPUP successfully")
                                    logger.info("TOPUP successfully")
                                    logger.debug(shift_detail)
                                
                                if status_code_tp != 201:
                                    logger.error("ERROR !!!")
                                    logger.debug(shift_detail)

                        # Participant not found   
                        if status_code == 404:
                            logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")

                            ptcpt_type = rowp.get('Participant_Type')
                            if ptcpt_type == 2:
                                template_id = template_ids["season_parker"]
                            elif ptcpt_type == 6:
                                template_id = template_ids["pmvc"]
                            elif ptcpt_type == 3:
                                template_id = template_ids["cmp"]

                            print(rowp)
                            
                            xml_ptcpt_data = consumer_to_xml(rowp)
                            logger.debug(xml_ptcpt_data)
                            status_code, result = create_participant(company_id, template_id, xml_ptcpt_data)
                            
                            if status_code == 201:
                                logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")

                                data = {
                                    "articles": [
                                        {
                                            "artClassRef": 0,
                                            "articleRef": 10624,
                                            "quantity": 1,
                                            "quantityExp": 0,
                                            "amount": 0,
                                            "influenceRevenue": 1,
                                            "influenceCashFlow": 1,
                                            "personalizedMoneyValueCard": {
                                                "ContractId": company_id,
                                                "ConsumerId": participant_id,
                                                "addMoneyValue": int(money_balance)
                                            }
                                        }
                                    ]
                                }
                        
                                if ptcpt_type == 6:
                                    print(f"------------------------------------ TOPUP for USER #{participant_id}#------------------------------------------ ")
                                    
                                    # Topup PMVC
                                    data_topup_xml = topup_pmvc_xml(shift_id, data)
                                    status_code_tp, shift_detail = topup_pmvc_api(shift_id, data_topup_xml)
                                    
                                    if status_code_tp == 200:
                                        logger.success("TOPUP successfully")
                                        logger.info("TOPUP successfully")
                                        logger.debug(shift_detail)
                                    
                                    if status_code_tp != 201:
                                        logger.error("ERROR !!!")
                                        logger.debug(shift_detail)
                                        
                                        print("--------------------------------------------------------------------------------------------------------------- ")

                            logger.info(f"Status code: {status_code}")
                            logger.debug(f"Status code: {status_code}")
                            logger.debug(result)
                            print("\n")
                            
                            if status_code == 500:
                                logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

                    # Close SHIFT
                    data_close = close_shift_xml(shift_id, shift_status)
                    status_code, shift_detail = close_shift_api(shift_id, data_close)

                    if status_code == 200:
                        logger.info(f"Close Shift for Shift ID {shift_id} successful")
                        logger.debug(f"Response {status_code} from Shift {shift_detail}")
                        
                    else:
                        logger.error(f"Error Occurred while closing Shift ID {shift_id}")
                        logger.debug(f"Response {status_code} from Shift {shift_detail}")

                else:
                    logger.error(f"Error Occurred while Opening Shift")
                    logger.debug(f"Response {status_code} from Shift {shift_detail}")
 """