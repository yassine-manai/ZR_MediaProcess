import xml.etree.ElementTree as ET
from xml.dom import minidom

""" class rowdata:
    cid: int
    cname: str
    ptcptname: str
    stardta: str
    
    
    "validatedate"
    def validate_stardta(self, format str):
        self.startta= "e" """
        
class XMLConverter:
    def __init__(self, data, namespace, root_element):
        self.data = data
        self.namespace = namespace
        self.root_element = root_element

    def to_xml(self):
        ET.register_namespace('', self.namespace)
        root = ET.Element(f"{{{self.namespace}}}{self.root_element}")

        self._add_elements(root, self.data)

        xml_str = ET.tostring(root, encoding='UTF-8', method='xml')
        return self._prettify(xml_str)

    def _add_elements(self, parent, data):

        for key, value in data.items():
            if isinstance(value, dict):
                element = ET.SubElement(parent, f"{{{self.namespace}}}{key}")
                self._add_elements(element, value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        element = ET.SubElement(parent, f"{{{self.namespace}}}{key}")
                        self._add_elements(element, item)
                    else:
                        element = ET.SubElement(parent, f"{{{self.namespace}}}{key}")
                        element.text = str(item)
            else:
                element = ET.SubElement(parent, f"{{{self.namespace}}}{key}")
                element.text = str(value)

    def _prettify(self, xml_str):
        reparsed = minidom.parseString(xml_str)
        pretty_xml = reparsed.toprettyxml(indent="   ", encoding="UTF-8").decode("UTF-8")
        return pretty_xml.replace('<?xml version="1.0"?>', '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')


class CompanyContract(XMLConverter):
    def __init__(self, data):
        super().__init__(data, "http://gsph.sub.com/cust/types", "contractDetail")


class ConsumerDetail(XMLConverter):
    def __init__(self, data):
        super().__init__(data, "http://gsph.sub.com/cust/types", "consumerDetail")


company_data = {
    "contract": {
        "id": 11,
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
    },
     "pooling": {
        "poolingDetail": {
            "extCardProfile": "Lac 1",
            "maxCounter": "Tunis",
            "poolingType": "666"
        }
    }
}


consumer_data = {
    "consumer": {
        "id": 3100,
        "contractid": 3,
        "name": "",
        "xValidFrom": "2020-01-01+01:00",
        "xValidUntil": "2025-01-01+01:00",
        "filialId": 1001
    },
    "person": {
        "firstName": "Antonio",
        "surname": "Rossi"
    },
    "identification": {
        "ptcptType": 6,
        "cardno": "123456",
        "cardclass": 0,
        "identificationType": 51,
        "validFrom": "2020-01-01+01:00",
        "validUntil": "2025-01-01+01:00",
        "usageProfile": {
            "href": "/usageProfile/1",
            "id": 1,
            "name": "Global Access",
            "description": ""
        },
        "admission": "",
        "ignorePresence": 0,
        "present": False,
        "status": 0,
        "ptcptGrpNo": -1,
        "chrgOvdrftAcct": 0
    },
    "displayText": -1,
    "limit": 9999900,
    "memo": "Note1",
    "status": 0,
    "delete": 0,
    "ignorePresence": 0,
    "lpn1": "AA000AA",
    "lpn2": "LPN22",
    "lpn3": "LPN33"
}


""" company_contract = CompanyContract(company_data).to_xml()
print("Company Contract XML:")
print(company_contract)

consumer_detail = ConsumerDetail(consumer_data).to_xml()
print("Consumer Detail XML:")
print(consumer_detail) """
