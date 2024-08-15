

from tkinter import messagebox
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from classes.error_except import ValidationException
from globals.global_vars import glob_vals
from dateutil.parser import parse, ParserError

date_formats = ["%d-%m-%Y", "%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"]


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
    def validate_positive_data(cls, value):
        try:
            value = int(value)  
        except (ValueError, TypeError):
            messagebox.showerror("Error", f"Compagny Id must be an integer between 1 and 99999, provided {value}")
            print(f"Compagny Id must be an integer between 1 and 99999, provided {value}")
        
        if value <= 1 or value > 99999:
            messagebox.showerror("Error", f"Company Id must be between 1 and 99999, provided {value}")
            print(f"Company Id must be between 1 and 99999, provided {value}")
        return value

    
    @field_validator('Company_ValidUntil', 'Company_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        global glob_vals
        
        non_empty_fields = ['Company_ValidUntil', 'Participant_ValidUntil']

        if info.field_name in non_empty_fields and value == '':
            print(info)
            messagebox.showerror("Error", f"{info.field_name} cannot be empty")
            print(f"{info.field_name} cannot be empty")

        if value == '':
            return value

        try:
            date_obj = parse(value, fuzzy=False)

            formatted_date = date_obj.strftime(glob_vals['date_format_val'])
            return formatted_date
        
        except (ParserError, ValueError) as e:
            messagebox.showerror("Error", f"Date format for '{value}' is not supported or invalid: {str(e)}")
            print(f"Date format for '{value}' is not supported or invalid: {str(e)}")


    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Company_id', 'Company_Name', 'Company_ValidUntil']

        for field in mandatory_fields:
            if not values.get(field):
                messagebox.showerror("Error", f"The field {field} is mandatory and cannot be empty.")
                print(f"The field {field} is mandatory and cannot be empty.")

        return values
    



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
    def validate_positive_data(cls, value):
        try:
            value = int(value)  
        except (ValueError, TypeError):
            messagebox.showerror("Error", f"Compagny Id must be an integer between 1 and 99999, provided {value}")
            print(f"Compagny Id must be an integer between 1 and 99999, provided {value}")
        
        if value < 1 or value > 99999:
            messagebox.showerror("Error", f"Compagny Id must be between 1 and 99999, provided {value}")
            print(f"Compagny Id must be between 1 and 99999, provided {value}")
        return value


    @field_validator('Participant_ValidUntil', 'Participant_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        if value == '':
            
            return KeyError

        try:
            date_obj = parse(value, fuzzy=False)

            formatted_date = date_obj.strftime(glob_vals['date_format_val'])
            return formatted_date
        
        except (ParserError, ValueError) as e:
            messagebox.showerror("Error", f"Date format for '{value}' is not supported or invalid: {str(e)}")
            print(f"Date format for '{value}' is not supported or invalid: {str(e)}")



    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Participant_Id', 'Participant_Firstname', 'Participant_Surname', 'Participant_CardNumber', 'Participant_LPN1', 'Company_id']

        for field in mandatory_fields:
            if not values.get(field):
                messagebox.showerror("Error", f"The field {field} is mandatory and cannot be empty.")
                print(f"The field {field} is mandatory and cannot be empty.")

        return values
    
    
    
    @field_validator('Participant_Type', mode='before')
    def validate_ptcpt_type(cls, value: int):
        if value not in [2, 6]:   
                messagebox.showerror("Error", f"Participant Type must be either 2 or 6, provided is {value}")
                print(f"Participant Type must be either 2 or 6, provided is {value}")
        return value
    
    
    
