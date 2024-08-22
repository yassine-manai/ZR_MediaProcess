

def contract_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml_content += '<cm:contractDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'

    # Contract section
    contract_fields = [
        ("cm:id", data.get("Company_id", "")),
        ("cm:name", data.get("Company_Name", "")),
        ("cm:xValidFrom", data.get("Company_ValidFrom", "")),
        ("cm:xValidUntil", data.get("Company_ValidUntil", ""))
    ]
    
    if any(value for _, value in contract_fields):
        xml_content += '<cm:contract>\n'
        for tag, value in contract_fields:
            if value:
                xml_content += f'<{tag}>{value}</{tag}>\n'
        xml_content += '</cm:contract>\n'

    # Person section
    person_fields = [
        ("cm:surname", data.get("Company_Surname", "")),
        ("cm:phone1", data.get("Company_phone1", "")),
        ("cm:email1", data.get("Company_email1", ""))
    ]
    
    if any(value for _, value in person_fields):
        xml_content += '<cm:person>\n'
        for tag, value in person_fields:
            if value:
                xml_content += f'<{tag}>{value}</{tag}>\n'
        xml_content += '</cm:person>\n'

    # Address section
    address_fields = [
        ("cm:street", data.get("Company_Street", "")),
        ("cm:town", data.get("Company_Town", "")),
        ("cm:postbox", data.get("Company_Postbox", ""))
    ]
    
    if any(value for _, value in address_fields):
        xml_content += '<cm:stdAddr>\n'
        for tag, value in address_fields:
            if value:
                xml_content += f'<{tag}>{value}</{tag}>\n'
        xml_content += '</cm:stdAddr>\n'

    xml_content += '</cm:contractDetail>'
    return xml_content

    
def consumer_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml_content += '<cm:consumerDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Consumer section
    consumer_fields = [
        ("cm:id", data.get("Participant_Id", "")),
        ("cm:contractid", data.get("Company_id", ""))
    ]
    
    if any(value for _, value in consumer_fields):
        xml_content += '<cm:consumer>\n'
        for tag, value in consumer_fields:
            if value:
                xml_content += f'<{tag}>{value}</{tag}>\n'
        xml_content += '</cm:consumer>\n'

    # Person section
    person_fields = [
        ("cm:firstName", data.get("Participant_Firstname", "")),
        ("cm:surname", data.get("Participant_Surname", ""))
    ]
    
    if any(value for _, value in person_fields):
        xml_content += '<cm:person>\n'
        for tag, value in person_fields:
            if value:
                xml_content += f'<{tag}>{value}</{tag}>\n'
        xml_content += '</cm:person>\n'

    # Identification section
    identification_fields = [
        ("cm:cardno", data.get("'Participant_CardNumber", "")),
        ("cm:validFrom", data.get("Participant_ValidFrom", "")),
        ("cm:validUntil", data.get("Participant_ValidUntil", "")),
        ("cm:ptcptGrpNo", data.get("Participant_GrpNo", "")),
        ("cm:status", data.get("Participant_Status", ""))
    ]
    
    usage_profile_id = data.get("usageProfileId", "")
    
    if any(value for _, value in identification_fields) or usage_profile_id:
        xml_content += '<cm:identification>\n'
        for tag, value in identification_fields:
            if value:
                xml_content += f'<{tag}>{value}</{tag}>\n'
                
        # UsageProfile section inside Identification
        if usage_profile_id:
            xml_content += '<cm:usageProfile>\n'
            xml_content += f'<cm:id>{usage_profile_id}</cm:id>\n'
            xml_content += '</cm:usageProfile>\n'
        
        xml_content += '</cm:identification>\n'
    
    # Additional fields
    additional_fields = [
        ("cm:lpn1", data.get("Participant_LPN1", "")),
        ("cm:lpn2", data.get("Participant_LPN2", "")),
        ("cm:lpn3", data.get("Participant_LPN3", "")),
        ("cm:userfield1", data.get("userfield1", ""))
    ]
    
    for tag, value in additional_fields:
        if value:
            xml_content += f'<{tag}>{value}</{tag}>\n'

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
