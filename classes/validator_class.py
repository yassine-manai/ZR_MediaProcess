from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from dateutil.parser import parse
from classes.error_except import CompanyValidationError, ConsumerValidationError
from globals.global_vars import glob_vals

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
            raise CompanyValidationError(f"Value {value} is out of range for {info.field_name}. Must be between 2 and 99999.")
        return value

    @field_validator('Company_ValidUntil', 'Company_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        global glob_vals
        
        if value:
            try:
                date_obj = parse(value, fuzzy=False)
                formatted_date = date_obj.strftime(glob_vals['date_format_val'])
                return formatted_date
            except ValueError:
                raise CompanyValidationError(f"Invalid date format for {info.field_name}. Must be in the format {glob_vals['date_format_val']}.")
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
    Participant_LPN1: str
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
    Participant_LPN2: Optional[str] = ''   
    Participant_LPN3: Optional[str] = ''

    @field_validator('Participant_Id', 'Company_FilialId', mode='before')
    def validate_positive_data(cls, value, info):
        value = int(value)
        if value < 1 or value > 99999:
            raise ConsumerValidationError(f" Value {value}  out of range for {info.field_name}. Must be between 1 and 99999.")
        return value



    @field_validator('Participant_ValidUntil', 'Participant_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):        
        global glob_vals

        if value:
            try:
                date_obj = parse(value, fuzzy=False)
                formatted_date = date_obj.strftime(glob_vals['date_format_val'])
                return formatted_date
            except ValueError:
                raise CompanyValidationError(f"Invalid date format for {info.field_name}. Must be in the format {glob_vals['date_format_val']}.")
        return value

    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Participant_Id', 'Participant_Firstname', 'Participant_Surname', 'Participant_CardNumber', 'Participant_LPN1', 'Company_id']
        for field in mandatory_fields:
            if not values.get(field):
                raise ConsumerValidationError(f"The field {field} is mandatory and cannot be empty.")
        return values

    @field_validator('Participant_Type', mode='before')
    def validate_ptcpt_type(cls, value: int):
        if value not in [2, 6]:
            raise ConsumerValidationError(f"Invalid value {value} for Participant_Type. Must be 2 or 6.")
        return value