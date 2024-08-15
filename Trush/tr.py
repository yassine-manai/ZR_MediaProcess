def load_file_data(self):
    path = self.path_entry.get()
    header_state = self.no_headers_var.get()  
    if not path:
        messagebox.showerror("Error", "Please enter a file path or choose a file.")
        return

    result = read_data_with_header(path, header=header_state)

    if result is None:
        messagebox.showerror("Error", "Failed to load the file.")
        return

    if header_state == False:
        # No headers, use the first row as headers and treat rest as data
        data = result
        if data:
            headers = data[0].keys()  # Assuming data is a list of dictionaries
        else:
            headers = []

    else:
        # Headers exist, extract them from the result
        headers, data = result if result else ([], [])

    if not data:
        messagebox.showwarning("Warning", "The file appears to be empty.")
        return

    # If headers exist, ensure that they are reflected in the dropdowns
    if headers:
        for label, dropdown in self.dropdowns:
            dropdown.configure(values=[""] + list(headers))
            dropdown.set("")

        self.header_dropdown.configure(values=[""] + list(headers))
        self.header_dropdown.set("")

    self.check_mandatory_fields()
    
    
    
    
    
    
            messagebox.showwarning("Warning", "The file appears to be empty.")

    
        messagebox.showerror("Error", "Please enter a file path or choose a file.")




----------------------------------------------------------------        ----------------------------------------------------------------



from tkinter import messagebox
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from classes.error_except import ValidationException
from globals.global_vars import glob_vals
from dateutil.parser import parse, ParserError

date_formats = ["%d-%m-%Y", "%d.%m.%Y", "%d:%m:%Y", "%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y"]

def validate(self):
    try:
        super().validate()
        return 200
    except ValidationException as e:
        self.errors.append(e)
        print(f"Error: {e}")
        return e.status_code
    
        

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
        try:
            value = int(value)  
        except (ValueError, TypeError):
            raise ValidationException(f"Company Id must be an integer between 1 and 99999, provided {value}", 500, info.field_name)
        
        if value <= 1 or value > 99999:
            raise ValidationException(f"Company Id must be between 1 and 99999, provided {value}", 500, info.field_name)
        return value

    @field_validator('Company_ValidUntil', 'Company_ValidFrom', mode='before')
    def validate_date_format(cls, value, info):
        global glob_vals

        non_empty_fields = ['Company_ValidUntil', 'Participant_ValidUntil']

        if info.field_name in non_empty_fields and value == '':
            raise ValidationException(f"{info.field_name} cannot be empty", 500, info.field_name)

        if value == '':
            return value

        try:
            date_obj = parse(value, fuzzy=False)
            formatted_date = date_obj.strftime(glob_vals['date_format_val'])
            return formatted_date
        
        except (ParserError, ValueError) as e:
            raise ValidationException(f"Date format for '{value}' is not supported or invalid: {str(e)}", 500, info.field_name)

    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Company_id', 'Company_Name', 'Company_ValidUntil']

        for field in mandatory_fields:
            if not values.get(field):
                raise ValidationException(f"The field {field} is mandatory and cannot be empty.", 500, field)

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
    def validate_positive_data(cls, value, info):
        try:
            value = int(value)  
        except (ValueError, TypeError):
            raise ValidationException(f"Company Id must be an integer between 1 and 99999, provided {value}", 500, info.field_name)
        
        if value < 1 or value > 99999:
            raise ValidationException(f"Company Id must be between 1 and 99999, provided {value}", 500, info.field_name)
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
            raise ValidationException(f"Date format for '{value}' is not supported or invalid: {str(e)}", 500, info.field_name)



    @model_validator(mode='before')
    def check_mandatory_fields(cls, values):
        mandatory_fields = ['Participant_Id', 'Participant_Firstname', 'Participant_Surname', 'Participant_CardNumber', 'Participant_LPN1', 'Company_id']

        for field in mandatory_fields:
            if not values.get(field):
                raise ValidationException(f"The field {field} is mandatory and cannot be empty.", 500, field)

        return values
    
    
    
    @field_validator('Participant_Type', mode='before')
    def validate_ptcpt_type(cls, value: int, info):
        if value not in [2, 6]:                
                raise ValidationException(f"Participant Type must be either 2 or 6, provided is {value}", 500, info)
        return value
    
    
    
