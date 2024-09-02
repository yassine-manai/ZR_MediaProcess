from collections import defaultdict
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

def processshift(body: str):
    # Look for the start and end of the <shiftId> tag
    shift_start = body.find('<shiftId>')
    shift_end = body.find('</shiftId>')
    
    # If both tags are found, extract the shiftId
    if shift_start > -1 and shift_end > shift_start:
        return body[shift_start + len('<shiftId>'):shift_end]
    
    return None
    


# --------------------------------------------------- SHIFTS PARSER --------------------------------

# OPEN SHIFT REPONSE PARSER 

def open_shift_response(response_dict):
    xml_string = response_dict.get('content', '')
    
    root = ET.fromstring(xml_string)
    
    # Find the shift element using the correct namespace
    shift = root.find('.//{http://gsph.sub.com/payment/types}shift')
    
    # Extract shift details
    shift_status = shift.findtext('{http://gsph.sub.com/payment/types}shiftStatus')
    shift_id = shift.findtext('{http://gsph.sub.com/payment/types}shiftId')
    shift_no = shift.findtext('{http://gsph.sub.com/payment/types}shiftNo')

    return shift_status, shift_id, shift_no


# GET CURRENT SHIFT REPONSE PARSER 
def current_shift_response(response_dict):
    xml_string = response_dict.get('content', '')

    # Parse the XML string
    root = ET.fromstring(xml_string)

    # Extract shift details using their specific tags
    shift_status = root.findtext('.//{http://gsph.sub.com/payment/types}shiftStatus')
    shift_id = root.findtext('.//{http://gsph.sub.com/payment/types}shiftId')
    shift_no = root.findtext('.//{http://gsph.sub.com/payment/types}shiftNo')

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

# --------------------------------------------------- TEMPLATES PARSER --------------------------------



def parse_templates_company(response):
    # Extract the XML content from the response
    xml_content = response.get('content', '')

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Extract the namespace from the root tag
    namespace = {'ns': root.tag.split('}')[0].strip('{')}

    # Initialize a list to store the templates
    templates = []

    # Iterate through each <template> element and extract the ID and name
    for template in root.findall('ns:template', namespace):
        template_id = template.find('ns:id', namespace).text
        template_name = template.find('ns:name', namespace).text
        templates.append({'id': template_id, 'name': template_name})

    return templates




def parse_template_consumer(response):
    # Extract the XML content from the response
    xml_content = response.get('content', '')

    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Extract the namespace from the root tag
    namespace = {'ns': root.tag.split('}')[0].strip('{')}

    # Initialize a dictionary to store the templates, allowing for multiple IDs per name
    templates = defaultdict(list)

    # Iterate through each <template> element and extract the ID and name
    for template in root.findall('ns:template', namespace):
        template_id = template.find('ns:id', namespace).text
        template_name = template.find('ns:name', namespace).text
        templates[template_name].append(template_id)

    # Convert defaultdict to a regular dict before returning
    return dict(templates)



                #self.template1_var = StringVar(value="3")
        #self.template2_var = StringVar(value="100")
        #self.template3_var = StringVar(value="2")
