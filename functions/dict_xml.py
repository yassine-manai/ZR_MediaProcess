

def contract_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml_content += '<cm:contractDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Contract section
    xml_content += '<cm:contract>\n'
    xml_content += f'<cm:id>{data.get("id", "")}</cm:id>\n'
    xml_content += f'<cm:name>{data.get("name", "")}</cm:name>\n'
    xml_content += f'<cm:xValidFrom>{data.get("xValidFrom", "")}</cm:xValidFrom>\n'
    xml_content += f'<cm:xValidUntil>{data.get("xValidUntil", "")}</cm:xValidUntil>\n'
    xml_content += '</cm:contract>\n'

    # Person section
    xml_content += '<cm:person>\n'
    xml_content += f'<cm:surname>{data.get("surname", "")}</cm:surname>\n'
    xml_content += f'<cm:phone1>{data.get("phone1", "")}</cm:phone1>\n'
    xml_content += f'<cm:email1>{data.get("email1", "")}</cm:email1>\n'
    xml_content += '</cm:person>\n'

    # Address section
    xml_content += '<cm:stdAddr>\n'
    xml_content += f'<cm:street>{data.get("street", "")}</cm:street>\n'
    xml_content += f'<cm:town>{data.get("town", "")}</cm:town>\n'
    xml_content += f'<cm:postbox>{data.get("postbox", "")}</cm:postbox>\n'
    xml_content += '</cm:stdAddr>\n'
    
    xml_content += '</cm:contractDetail>'
    return xml_content

    
def consumer_to_xml(data):
    xml_content = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    xml_content += '<cm:consumerDetail xmlns:cm="http://gsph.sub.com/cust/types">\n'
    
    # Consumer section
    xml_content += '<cm:consumer>\n'
    xml_content += f'<cm:id>{data.get("id", "")}</cm:id>\n'
    xml_content += f'<cm:contractid>{data.get("contractid", "")}</cm:contractid>\n'
    xml_content += '</cm:consumer>\n'
    
    # Person section
    xml_content += '<cm:person>\n'
    xml_content += f'<cm:firstName>{data.get("firstName", "")}</cm:firstName>\n'
    xml_content += f'<cm:surname>{data.get("surname", "")}</cm:surname>\n'
    xml_content += '</cm:person>\n'
    
    # Identification section
    xml_content += '<cm:identification>\n'
    xml_content += f'<cm:cardno>{data.get("cardno", "")}</cm:cardno>\n'
    xml_content += f'<cm:validFrom>{data.get("validFrom", "")}</cm:validFrom>\n'
    xml_content += f'<cm:validUntil>{data.get("validUntil", "")}</cm:validUntil>\n'
    
    # UsageProfile section inside Identification
    xml_content += '<cm:usageProfile>\n'
    xml_content += f'<cm:id>{data.get("usageProfileId", "")}</cm:id>\n'
    xml_content += '</cm:usageProfile>\n'
    
    xml_content += f'<cm:ptcptGrpNo>{data.get("ptcptGrpNo", "")}</cm:ptcptGrpNo>\n'
    xml_content += f'<cm:status>{data.get("status", "")}</cm:status>\n'
    xml_content += '</cm:identification>\n'
    
    # Additional fields
    xml_content += f'<cm:lpn1>{data.get("lpn1", "")}</cm:lpn1>\n'
    xml_content += f'<cm:lpn2>{data.get("lpn2", "")}</cm:lpn2>\n'
    xml_content += f'<cm:lpn3>{data.get("lpn3", "")}</cm:lpn3>\n'
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
