from config.config import *
from datetime import datetime

current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def open_shift_xml():
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<pay:shift xmlns:pay="http://gsph.sub.com/payment/types">\n'

    # Shift details section
    shift_fields = [
        ("pay:computerId", COMPUTER_ID),
        ("pay:deviceId", DEVICE_ID),
        ("pay:cashierContractId", CASHIER_CONTRACT_ID),
        ("pay:cashierConsumerId", CASHIER_CONSUMER_ID),
        ("pay:shiftNo", 1),
        ("pay:createDateTime", current_datetime)
    ]
    
    for tag, value in shift_fields:
        if value:
            xml_content += f'<{tag}>{value}</{tag}>\n'

    xml_content += '</pay:shift>'
    return xml_content

def close_shift_xml(shiftId, shiftStatus):

    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<pay:shift xmlns:pay="http://gsph.sub.com/payment/types">\n'
    xml_content += f'<pay:shiftId>{shiftId}</pay:shiftId>\n'
    xml_content += f'<pay:computerId>{COMPUTER_ID}</pay:computerId>\n'
    xml_content += f'<pay:deviceId>{DEVICE_ID}</pay:deviceId>\n'
    xml_content += f'<pay:cashierContractId>{CASHIER_CONTRACT_ID}</pay:cashierContractId>\n'
    xml_content += f'<pay:cashierConsumerId>{CASHIER_CONSUMER_ID}</pay:cashierConsumerId>\n'
    xml_content += f'<pay:finishDateTime>{current_datetime}</pay:finishDateTime>\n'
    xml_content += f'<pay:shiftStatus>{shiftStatus}</pay:shiftStatus>\n'
    xml_content += '</pay:shift>'

    return xml_content


def topup_pmvc_xml(shift_id, data):
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<pay:salesTransactionDetail xmlns:pay="http://gsph.sub.com/payment/types">\n'
    
    # Sales Transaction section
    xml_content += '    <pay:salesTransaction>\n'
    sales_transaction_fields = [
        ("pay:shiftId", shift_id),
        ("pay:computerId", COMPUTER_ID),
        ("pay:deviceId", DEVICE_ID),
        ("pay:cashierContractId", CASHIER_CONTRACT_ID),
        ("pay:cashierConsumerId", CASHIER_CONSUMER_ID),
        ("pay:salesTransactionDateTime", current_datetime)
    ]
    
    for tag, value in sales_transaction_fields:
        if value:
            xml_content += f'        <{tag}>{value}</{tag}>\n'
    xml_content += '    </pay:salesTransaction>\n'
    
    # Articles section
    xml_content += '    <pay:articles>\n'
    for article in data.get("articles", []):
        xml_content += '        <pay:article>\n'
        article_fields = [
            ("pay:artClassRef", article.get("artClassRef", 0)),
            ("pay:articleRef", article.get("articleRef", 10601)),
            ("pay:quantity", article.get("quantity", 0)),
            ("pay:quantityExp", article.get("quantityExp", 0)),
            ("pay:amount", article.get("amount", 0)),
            ("pay:influenceRevenue", article.get("influenceRevenue", 0)),
            ("pay:influenceCashFlow", article.get("influenceCashFlow", 0))
        ]
        
        for tag, value in article_fields:
            xml_content += f'            <{tag}>{value}</{tag}>\n'
        
        card = article.get("personalizedMoneyValueCard", {})
        if card:
            xml_content += '            <pay:personalizedMoneyValueCard>\n'
            card_fields = [
                ("pay:ContractId", card.get("ContractId", "")),
                ("pay:ConsumerId", card.get("ConsumerId", "")),
                ("pay:addMoneyValue", card.get("addMoneyValue", ""))
            ]
            
            for tag, value in card_fields:
                if value:
                    xml_content += f'                <{tag}>{value}</{tag}>\n'
            xml_content += '            </pay:personalizedMoneyValueCard>\n'
        
        xml_content += '        </pay:article>\n'
    xml_content += '    </pay:articles>\n'
    
    xml_content += '</pay:salesTransactionDetail>'
    return xml_content
