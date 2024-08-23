

def contract_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml_content += '<cm:contractDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Contract section
    contract_content = ''
    if data.get("Company_id"):
        contract_content += f'    <cm:id>{data.get("Company_id")}</cm:id>\n'
    if data.get("Company_Name"):
        contract_content += f'    <cm:name>{data.get("Company_Name")}</cm:name>\n'
    if data.get("Company_ValidFrom"):
        contract_content += f'    <cm:xValidFrom>{data.get("Company_ValidFrom")}</cm:xValidFrom>\n'
    if data.get("Company_ValidUntil"):
        contract_content += f'    <cm:xValidUntil>{data.get("Company_ValidUntil")}</cm:xValidUntil>\n'
    
    if contract_content:
        xml_content += '<cm:contract>\n' + contract_content + '  </cm:contract>\n'
    
    # Person section
    person_content = ''
    if data.get("Company_Surname"):
        person_content += f'    <cm:surname>{data.get("Company_Surname")}</cm:surname>\n'
    if data.get("Company_phone1"):
        person_content += f'    <cm:phone1>{data.get("Company_phone1")}</cm:phone1>\n'
    if data.get("Company_email1"):
        person_content += f'    <cm:email1>{data.get("Company_email1")}</cm:email1>\n'
    
    if person_content:
        xml_content += '<cm:person>\n' + person_content + '  </cm:person>\n'
    
    # Address section
    address_content = ''
    if data.get("Company_Street"):
        address_content += f'    <cm:street>{data.get("Company_Street")}</cm:street>\n'
    if data.get("Company_Town"):
        address_content += f'    <cm:town>{data.get("Company_Town")}</cm:town>\n'
    if data.get("Company_Postbox"):
        address_content += f'    <cm:postbox>{data.get("Company_Postbox")}</cm:postbox>\n'
    
    if address_content:
        xml_content += '<cm:stdAddr>\n' + address_content + '  </cm:stdAddr>\n'
    
    xml_content += '</cm:contractDetail>'
    return xml_content


data = {
    'Participant_Id': 1,
    'Participant_Firstname': 'Stuart',
    'Participant_Surname': 'Chriscoli',
    'Participant_CardNumber': '1',
    'Participant_LPN1': 'ABC123',
    'Company_id': 144,
    'Company_FilialId': 7001,
    'Participant_Type': 6,
    'Participant_Cardclass': '',
    'Participant_IdentificationType': '',
    'Participant_ValidFrom': '',
    'Participant_ValidUntil': '2025-01-01+01:00',
    'Participant_Status': 0,
    'Participant_GrpNo': None,
    'Participant_Present': '',
    'Participant_DisplayText': '',
    'Participant_LPN2': '',
    'Participant_LPN3': '',
    'Money_Balance': '500'
}

def consumer_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml_content += '<cm:consumerDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Consumer section
    xml_content += '<cm:consumer>\n'
    xml_content += f'<cm:id>{data.get("Participant_Id", "")}</cm:id>\n'
    xml_content += f'<cm:contractid>{data.get("Company_id", "")}</cm:contractid>\n'
    xml_content += '</cm:consumer>\n'
    
    # Person section
    xml_content += '<cm:person>\n'
    xml_content += f'<cm:firstName>{data.get("Participant_Firstname", "")}</cm:firstName>\n'
    xml_content += f'<cm:surname>{data.get("Participant_Surname", "")}</cm:surname>\n'
    xml_content += '</cm:person>\n'
    
    # Identification section
    xml_content += '<cm:identification>\n'
    xml_content += f'<cm:ptcptType>{data.get("Participant_Type", "")}</cm:ptcptType>\n'
    xml_content += f'<cm:cardno>{data.get("Participant_CardNumber", "")}</cm:cardno>\n'
    xml_content += f'<cm:validFrom>{data.get("Participant_ValidFrom", "")}</cm:validFrom>\n'
    xml_content += f'<cm:validUntil>{data.get("Participant_ValidUntil", "")}</cm:validUntil>\n'
    
    # UsageProfile section inside Identification
    xml_content += '<cm:usageProfile>\n'
    xml_content += f'<cm:id>{1}</cm:id>\n'
    xml_content += '</cm:usageProfile>\n'
    
    xml_content += f'<cm:ptcptGrpNo>{data.get(-1, "")}</cm:ptcptGrpNo>\n'
    xml_content += f'<cm:status>{data.get(0, "0")}</cm:status>\n'
    xml_content += '</cm:identification>\n'
    
    # Additional fields
    xml_content += f'<cm:lpn1>{data.get("Participant_LPN1", "")}</cm:lpn1>\n'
    xml_content += f'<cm:lpn2>{data.get("Participant_LPN2", "")}</cm:lpn2>\n'
    xml_content += f'<cm:lpn3>{data.get("Participant_LPN3", "")}</cm:lpn3>\n'
    xml_content += f'<cm:userfield1>{data.get("userfield1", "")}</cm:userfield1>\n'
    
    xml_content += '</cm:consumerDetail>'
    return xml_content




data_consumer = {
        "id": "25",
        "contractid": "214",
        "xValidFrom": '1900-01-01+01:00',
        "xValidUntil": '2025-01-01+01:00',
        "filialId": '7077',
        
        "firstName":'Participant_Firstname',
        "surname": 'Participant_Surname',
        "ptcptType": 'Participant_Type',
        "cardno": "E542",
        "cardclass": 'Participant_Cardclass',
        "identificationType": 'Participant_IdentificationType',
        "validFrom": '2020-01-01+01:00',
        "validUntil": '2025-01-01+01:00',
        "admission": "",
        "ignorePresence": '0',
        "present": 'false',
        "status": '0',
        "ptcptGrpNo": '-1',
        
        "displayText": '-1',
        "limit": '9999900',
        "memo": "Note1",
        "status": '0',
        "delete": '0',
        "ignorePresence":'0',
        "lpn1": 'NOLPN',
        "lpn2": 'NOLPN',
        "lpn3": 'NOLPN',
}



data_contract = {
    "contract": {
        "id": "11",
        "name": "MG",
        "xValidFrom": "2021-01-01",
        "xValidUntil": "2021-12-31"
    },
    "person": {
        "surname": "Groupe Me",
        "phone1": "76111111",
        "email1": "Monoprix@mail.tn"
    },
    "stdAddr": {
        "street": "Lac 1",
        "town": "Tunis",
        "postbox": "666"
    }
}

""" xml_company = contract_to_xml(data_contract)

print(xml_company)
 """

#xml_consumer = consumer_to_xml(data_consumer)
#print(xml_consumer) 


data = {
    'Participant_Id': 1,
    'Participant_Firstname': 'Stuart',
    'Participant_Surname': 'Chriscoli',
    'Participant_CardNumber': '1',
    'Participant_LPN1': 'ABC123',
    'Company_id': 144,
    'Company_FilialId': 7001,
    'Participant_Type': 6,
    'Participant_Cardclass': '',
    'Participant_IdentificationType': '',
    'Participant_ValidFrom': '',
    'Participant_ValidUntil': '2025-01-01+01:00',
    'Participant_Status': 0,
    'Participant_GrpNo': None,
    'Participant_Present': '',
    'Participant_DisplayText': '',
    'Participant_LPN2': '',
    'Participant_LPN3': '',
    'Money_Balance': '500'
}


xml_consumer = consumer_to_xml(data_consumer)
print(xml_consumer)