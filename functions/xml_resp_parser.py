import xml.etree.ElementTree as ET

def company_xml_parser(response):
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
    
    
    
    

def consumer_xml_parser(response):
    # Check if the response has a status code 200 and content type is XML
    if response['status_code'] == 200 and 'xml' in response['headers']['Content-Type']:
        # Parse the XML content
        root = ET.fromstring(response['content'])

        namespace = {'ns': 'http://gsph.sub.com/cust/types'}
        
        # Extract the required data from the consumer element
        consumer = root.find('ns:consumer', namespace)
        if consumer is not None:
            id = consumer.find('ns:id', namespace).text
            contractid = consumer.find('ns:contractid', namespace).text
            xValidFrom = consumer.find('ns:xValidFrom', namespace).text
            xValidUntil = consumer.find('ns:xValidUntil', namespace).text
            filialId = consumer.find('ns:filialId', namespace).text

            # Return the data as a tuple
            return (id, contractid, xValidFrom, xValidUntil, filialId)
        else:
            raise ValueError("Consumer element not found in the XML content.")
    else:
        raise ValueError("Invalid response format or status code.")
