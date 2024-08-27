from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from classes.error_except import CompanyValidationError, ConsumerValidationError
from globals.global_vars import glob_vals
from config.log_config import logger


class Company_validation(BaseModel):
    # Mandatory fields
    Company_id: int
    Company_Name: str
    Company_ValidUntil: str

    # Optional fields
    Company_ValidFrom: Optional[str] = ''
    Company_FilialId: Optional[int] = ''
    Company_Surname: Optional[str] = ''
    Company_phone1: Optional[str] = ''
    Company_email1: Optional[str] = ''
    Company_Street: Optional[str] = ''   
    Company_Town: Optional[str] = ''
    Company_Postbox: Optional[str] = ''   

    @field_validator('Company_id', 'Company_FilialId', mode='before')
    def validate_positive_data(cls, value, info):
        value = int(value)
        if value <= 1 or value > 99999:
            raise CompanyValidationError(f"Value {value} is out of range for {info.field_name}. \n Must be between 2 and 99999.")
        return value

    @field_validator('Company_ValidUntil', 'Company_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        global glob_vals
        init_format = glob_vals['date_format_val']
        logger.info(f" Date Format selected by user : {init_format}")
        if value:
            try:
                date_obj = datetime.strptime(value, init_format)
                return date_obj.strftime("%Y-%m-%d")
            
            except ValueError:
                raise CompanyValidationError(f"Invalid date format for {info.field_name}. \n Data values in CSV file must be in selected format : {init_format}\n. Check your file or check your selected Date fromat ")
            
        return value

    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Company_id', 'Company_Name', 'Company_ValidUntil']
        for field in mandatory_fields:
            if not values.get(field):
                raise CompanyValidationError(f"The field {field} is mandatory and cannot be empty.")
        return values



from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from dateutil.parser import parse

class Consumer_validation(BaseModel):
    # Mandatory fields
    Participant_Id: int
    Participant_Firstname: str
    Participant_Surname: str
    Participant_CardNumber: str
    Company_id: int
    
    # Optional fields
    Company_FilialId: Optional[int] = 7001
    Participant_Type: Optional[int] = 2
    Participant_Cardclass: Optional[str] = ''
    Participant_IdentificationType: Optional[str] = ''
    Participant_ValidFrom: Optional[str] = ''
    Participant_ValidUntil: Optional[str] = ''
    Participant_Status: Optional[int] = 0
    Participant_GrpNo: Optional[int] = None   
    Participant_Present: Optional[str] = ''
    Participant_DisplayText: Optional[str] = ''
    Participant_LPN1: Optional[str] = ''   
    Participant_LPN2: Optional[str] = ''   
    Participant_LPN3: Optional[str] = ''
    Amount: Optional[int] = 0

    @field_validator('Participant_Id', 'Company_FilialId', mode='before')
    def validate_positive_data(cls, value, info):
        value = int(value)
        if value < 1 or value > 99999:
            raise ConsumerValidationError(f" Value {value}  out of range for {info.field_name}. Must be between 1 and 99999.")
        return value



    @field_validator('Participant_ValidUntil', 'Participant_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):        
        global glob_vals
        init_format = glob_vals['date_format_val']
        logger.info(f" Date Format selected by user : {init_format}")
        if value:
            try:
                date_obj = datetime.strptime(value, init_format)
                return date_obj.strftime("%Y-%m-%d")
            
            except ValueError:
                raise CompanyValidationError(f"Invalid date format for {info.field_name}. \n Data values in CSV file must be in selected format : {init_format}\n Check your file or check your selected Date fromat ")
            
        return value

    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Participant_Id','Participant_ValidUntil','Participant_ValidFrom', 'Participant_Firstname', 'Participant_Surname', 'Participant_CardNumber', 'Company_id']
        for field in mandatory_fields:
            if not values.get(field):
                raise ConsumerValidationError(f"The field {field} is mandatory and cannot be empty.")
        return values
    
    @field_validator('Participant_Type', mode='before')
    def validate_ptcpt_type(cls, value: str) -> int:
        try:
            int_value = int(value)
        except ValueError:
            raise ConsumerValidationError("Participant_Type must be a valid integer.")
        
        # Ensure the integer value is either 2 or 6
        if int_value not in [2, 6]:
            raise ConsumerValidationError(f"Invalid value {int_value} for Participant_Type. Must be 2 or 6.")
        
        return int_value
    
    
"""     @field_validator('Amount', mode='before')
    def validate_amount(cls, value: str) -> int:
        try:
            int_value = int(value)
        except ValueError:
            raise ConsumerValidationError("Participant_Type must be a valid integer.")
        
        # Ensure the integer value is either 2 or 6
        if int_value == 0:
            raise ConsumerValidationError(f"Invalid value {int_value} for Participant_Type. Must be 2 or 6.")
        
        return int_value """
    
    
    