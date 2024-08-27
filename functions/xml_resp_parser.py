import xml.etree.ElementTree as ET


# ------------------------------------------------ PROCESS DATA PARSER ----------------------------------------------------------------

# COMPANY CREATE REPONSE PARSER 
def company_reponse_parser(response):
    # Check if the response has a status code 200 and content type is XML
    if response['status_code'] == 200 and 'xml' in response['headers']['Content-Type']:
        # Parse the XML content
        root = ET.fromstring(response['content'])

        namespace = {'ns': 'http://gsph.sub.com/cust/types'}
        
        # Extract the required data
        contract = root.find('ns:contract', namespace)
        if contract is not None:
            id = contract.find('ns:id', namespace).text
            name = contract.find('ns:name', namespace).text
            xValidFrom = contract.find('ns:xValidFrom', namespace).text
            xValidUntil = contract.find('ns:xValidUntil', namespace).text
            filialId = contract.find('ns:filialId', namespace).text

            # Return the data as a tuple
            return (id, name, xValidFrom, xValidUntil, filialId)
        else:
            raise ValueError("Contract element not found in the XML content.")
    else:
        raise ValueError("Invalid response format or status code.")
    
    
    
    
# PARTICIPANT CREATE REPONSE PARSER 
def participant_response_parser(response):
    # Check if the response has a status code 200 and content type is XML
    if response['status_code'] == 200 and 'xml' in response['headers']['Content-Type']:
        # Parse the XML content
        root = ET.fromstring(response['content'])

        namespace = {'ns': 'http://gsph.sub.com/cust/types'}
        
        # Extract the required data from the consumer element
        consumer = root.find('ns:consumer', namespace)
        if consumer is not None:
            ptcpt_id = consumer.find('ns:id', namespace).text
            contractid = consumer.find('ns:contractid', namespace).text
            xValidFrom = consumer.find('ns:xValidFrom', namespace).text
            xValidUntil = consumer.find('ns:xValidUntil', namespace).text
            filialId = consumer.find('ns:filialId', namespace).text

        person = root.find('ns:consumer', namespace)
        if person is not None:
            name = person.find('ns:firstName', namespace).text
            surname = person.find('ns:surname', namespace).text  
            
            # Return the data as a tuple
            return (ptcpt_id, contractid, name, surname, xValidFrom, xValidUntil, filialId)
        else:
            raise ValueError("Consumer element not found in the XML content.")
            pass
    else:
        raise ValueError("Invalid response format or status code.")

def processshift(body: dict):
    # <shiftId>1724675591</shiftId>
    shift=body.find('<shiftId>')
    shiftend=body.find('</shiftId>')
    if shift > -1 and shiftend > shift:
        return body[shift+len('<shiftId>'):shiftend]
    


# --------------------------------------------------- SHIFTS PARSER --------------------------------

# OPEN SHIFT REPONSE PARSER 

def open_shift_response(response_dict):
    xml_string = response_dict.get('content', '')
    
    # Parse the XML string
    root = ET.fromstring(xml_string)
    
    # Define namespace for finding elements
    namespace = {'ns': 'http://gsph.sub.com/payment/types'}
    
    # Find the shift element using the namespace
    shift = root.find('.//ns:shift', namespaces=namespace)
    
    # Extract shift details
    shift_status = shift.findtext('ns:shiftStatus', default='Unknown', namespaces=namespace)
    shift_id = shift.findtext('ns:shiftId', default='Unknown', namespaces=namespace)
    shift_no = shift.findtext('ns:shiftNo', default='Unknown', namespaces=namespace)

    return shift_status, shift_id, shift_no

# GET CURRENT SHIFT REPONSE PARSER 
def current_shift_response(response_dict):
    xml_string = response_dict.get('content', '')

    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Find the first shift element
    shift = root.find('.//{http://gsph.sub.com/payment/types}shift')
    if shift is not None:
        # Extract shift details
        shift_status = shift.findtext('{http://gsph.sub.com/payment/types}shiftStatus')
        shift_id = shift.findtext('{http://gsph.sub.com/payment/types}shiftId')
        shift_no = shift.findtext('{http://gsph.sub.com/payment/types}shiftNo')

        return shift_status, shift_id, shift_no






def get_status_code(response: dict) -> int:
    content = response.get('content', '')
    
    # Check if content is empty or contains a malformed XML tag
    if not content.strip() or '<shiftsxmlns=' in content:
        return 500
    
    try:
        # Attempt to parse the XML to ensure it is well-formed
        root = ET.fromstring(content)
        # Check for the presence of the expected elements
        if root.tag.endswith('shifts') and root.find('.//{http://gsph.sub.com/payment/types}shift') is not None:
            return 200
        else:
            return 500
    except ET.ParseError:
        return 500

# --------------------------------------------------- PAYMENTS PARSER --------------------------------
# TOPUP PMVC REPONSE PARSER 