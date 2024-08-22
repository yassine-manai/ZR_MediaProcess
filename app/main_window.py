import os
import customtkinter as ctk
from tkinter import StringVar, filedialog, messagebox
from api.api_media import create_company, create_participant, get_company_details, get_participant
from classes.error_except import CompanyValidationError, ConsumerValidationError
from functions.business_logic import get_data
from functions.load_data import read_data, read_data_with_header
from classes.validator_class import Company_validation, Consumer_validation
from config.log_config import logger
from functions.data_format import generate_unique_random
from functions.dict_xml import consumer_to_xml, contract_to_xml
from functions.test_connect import test_zr_connection
from functions.xml_resp_parser import company_xml_parser
from globals.global_vars import data_csv, zr_data, glob_vals


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

mandatory_columns = [
    "Company_id", "Company_Name", "Company_ValidUntil", "Participant_Id",
    "Participant_Firstname", "Participant_Surname",
    "Participant_CardNumber", "Participant_LPN1"
]
optional_columns = [
    "Company_ValidFrom", "Company_Surname", "Company_phone1", "Company_email1", "Company_Street", "Company_Town",
    "Company_Postbox","Company_FilialId" "Participant_FilialId", "Participant_Type",
    "Participant_Cardclass", "Participant_IdentificationType", "Participant_ValidFrom", "Participant_ValidUntil",
    "Participant_Present", "Participant_Status", "Participant_GrpNo",
    "Participant_DisplayText", "Participant_LPN2", "Participant_LPN3"
]

date_format_dict = {
    "dd-mm-yyyy": "%d-%m-%Y",
    "dd.mm.yyyy": "%d.%m.%Y",
    "dd/mm/yyyy": "%d/%m/%Y",
    
    "mm-dd-yyyy": "%m-%d-%Y",
    "mm.dd.yyyy": "%m.%d.%Y",
    "mm/dd/yyyy": "%m/%d/%Y",
    
    "yyyy-mm-dd": "%Y-%m-%d",
    "yyyy.mm.dd": "%Y.%m.%d",
    "yyyy/mm/dd": "%Y/%m/%d",
} 

rows_data = []


class CSVLoaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        logger.info("Starting Process & user interface . . . ")

        self.title("Customer Media Processor")
        self.geometry("1300x700")
        
        self.optional_field_count = 0
        self.optional_fields = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.create_file_input_frame()
        self.create_mandatory_fields_frame()
        self.create_optional_fields_frame()
        self.create_sync_button()
        self.create_footer_frame()


    def update_load_button_state(self, event=None):
        path = self.path_entry.get().strip()
        if path:
            self.load_data_button.configure(state="normal")
        else:
            self.load_data_button.configure(state="disabled")
            
    def create_file_input_frame(self):
        file_data_frame = ctk.CTkFrame(self.main_frame)
        file_data_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # File path input section
        ctk.CTkLabel(file_data_frame, text="File Path:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.path_entry = ctk.CTkEntry(file_data_frame, width=400)
        self.path_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.path_entry.bind("<KeyRelease>", self.update_load_button_state)  # Bind key release to update button state

        self.browse_button = ctk.CTkButton(file_data_frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.no_headers_var = ctk.BooleanVar(value=False)
        self.no_headers_check = ctk.CTkCheckBox(file_data_frame, text="No Headers", variable=self.no_headers_var)
        self.no_headers_check.grid(row=0, column=3, padx=5, pady=5)

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data", command=self.load_file_data, state="disabled")
        self.load_data_button.grid(row=0, column=4, padx=5, pady=5)

        # Template ID section
        ctk.CTkLabel(file_data_frame, text="Template ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Season Parker ID
        ctk.CTkLabel(file_data_frame, text="Season Parker ID:").grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.template1_var = StringVar(value="1")
        self.template1_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template1_var, width=50)
        self.template1_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # PMVC ID
        ctk.CTkLabel(file_data_frame, text="PMVC ID:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.template2_var = StringVar(value="2")
        self.template2_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template2_var, width=50)
        self.template2_entry.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

        # CPM ID
        ctk.CTkLabel(file_data_frame, text="CPM ID:").grid(row=1, column=5, padx=5, pady=5, sticky="e")
        self.template3_var = StringVar(value="3")
        self.template3_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template3_var, width=50)
        self.template3_entry.grid(row=1, column=6, padx=5, pady=5, sticky="ew")

        # Date Format
        ctk.CTkLabel(file_data_frame, text="Date Format:").grid(row=1, column=7, padx=5, pady=5, sticky="e")
        self.date_format_var = StringVar(value="yyyy-mm-dd")
        self.date_format_dropdown = ctk.CTkOptionMenu(file_data_frame, variable=self.date_format_var,
                                                    values=list(date_format_dict.keys()), width=100,
                                                    command=self.update_date_format)
        self.date_format_dropdown.grid(row=1, column=8, padx=5, pady=5, sticky="ew")

        file_data_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)


        # global variable values
        #self.update_global_values()

    def update_date_format(self, selected_format):
        global glob_vals
        glob_vals['date_format_val'] = date_format_dict.get(selected_format, '%d-%m-%Y')
        logger.info(f"Date Format updated to: {glob_vals['date_format_val']}")

    def update_global_values(self):
        global glob_vals
        selected_format = self.date_format_var.get()
        glob_vals['date_format_val'] = date_format_dict.get(selected_format, '%d-%m-%Y')
        glob_vals['season_parker'] = self.template1_var.get()
        glob_vals['pmvc'] = self.template2_var.get()
        glob_vals['cmp'] = self.template3_var.get()
        
        
        template_id1 = int(glob_vals['season_parker'])
        template_id2 = int(glob_vals['pmvc'])
        template_id3 = int(glob_vals['cmp'])
        logger.info(f"------------ {glob_vals['date_format_val']}")
        logger.info(f"Template ID updated to: {template_id1} -- {template_id2} -- {template_id3}")

    def create_mandatory_fields_frame(self):
        mandatory_frame = ctk.CTkFrame(self.main_frame)
        mandatory_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        mandatory_frame.grid_columnconfigure((1, 3, 5, 7, 9), weight=1)

        ctk.CTkLabel(mandatory_frame, text="Mandatory Fields", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=10, pady=10)

        self.dropdowns = []
        for i, label in enumerate(mandatory_columns):
            row = (i // 4) + 1
            col = (i % 4) * 2

            ctk.CTkLabel(mandatory_frame, text=label).grid(row=row, column=col, padx=5, pady=5, sticky="w")
            dropdown = ctk.CTkOptionMenu(mandatory_frame, width=150,values="", command=self.check_mandatory_fields)
            dropdown.grid(row=row, column=col+1, padx=5, pady=5, sticky="ew")
            dropdown.set("- - - - - - - - -")
            self.dropdowns.append((label, dropdown))

    def create_optional_fields_frame(self):
        optional_frame = ctk.CTkFrame(self.main_frame)
        optional_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        optional_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(optional_frame, text="Optional Fields", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        self.optional_field_var = ctk.StringVar()
        self.optional_field_dropdown = ctk.CTkOptionMenu(optional_frame, variable=self.optional_field_var, values=["No optional field"] + optional_columns, width=150)
        self.optional_field_dropdown.grid(row=1, column=0, padx=5, pady=5)
        self.optional_field_dropdown.set("No optional field")

        self.header_var = ctk.StringVar()
        self.header_dropdown = ctk.CTkOptionMenu(optional_frame, variable=self.header_var, values=[""], width=150)
        self.header_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.header_dropdown.set("No Column selected")

        add_button = ctk.CTkButton(optional_frame, text="+", width=30, command=self.add_optional_field)
        add_button.grid(row=1, column=2, padx=5, pady=5)

        self.optional_fields_container = ctk.CTkFrame(optional_frame,height=0)
        self.optional_fields_container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.optional_fields_container.grid_columnconfigure((0, 1, 2), weight=1)

    def create_sync_button(self):
        sync_frame = ctk.CTkFrame(self.main_frame)
        sync_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
        sync_frame.grid_columnconfigure(0, weight=1)

        self.sync_button = ctk.CTkButton(sync_frame, text="Sync", command=self.Main_Process, state="disabled")
        self.sync_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")
  
    def custom_retry_continue_dialog(self,title, message):
        dialog = ctk.CTkToplevel()
        dialog.title(title)
        dialog.geometry("500x200")
        
        response = None
        
        def on_continue():
            nonlocal response
            response = "continue"
            dialog.destroy()

        def on_exit():
            nonlocal response
            response = "exit"
            dialog.destroy()
        
        ctk.CTkLabel(dialog, text=message, wraplength=400).pack(pady=10)
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)

        retry_button = ctk.CTkButton(button_frame, text="Continue", command=on_continue)
        retry_button.pack(side='left', padx=10)

        continue_button = ctk.CTkButton(button_frame, text="Exit", command=on_exit)
        continue_button.pack(side='right', padx=10)
        
        dialog.grab_set() 
        dialog.wait_window()

        return response

    def create_footer_frame(self):
        footer_frame = ctk.CTkFrame(self.main_frame)
        footer_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        footer_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)  

        entries = [
            ("ZR IP", "zr_ip"),
            ("ZR Port", "zr_port"),
            ("Username", "username"),
            ("Password", "password")
        ]

        for i, (label, attr) in enumerate(entries):
            ctk.CTkLabel(footer_frame, text=label).grid(row=0, column=2 * i, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(footer_frame)

            entry.insert(0, zr_data.get(attr, ""))  
            entry.grid(row=0, column=2 * i + 1, padx=5, pady=5, sticky="ew")
            setattr(self, attr, entry)


        #self.confirm_button = ctk.CTkButton(footer_frame, text="Test & Confirm", command=self.test_confirm)
        self.confirm_button = ctk.CTkButton(footer_frame, text="Test & Confirm", command=self.Main_Process)
        self.confirm_button.grid(row=0, column=8, padx=5, pady=10, sticky="e")

    def browse_file(self):
        logger.debug("Selecting file process started...")       
        try:
            filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

            if filename:
                self.path_entry.delete(0, ctk.END)
                self.path_entry.insert(0, filename)
                self.load_data_button
                self.load_data_button.configure(state="normal")

                logger.success(f"CSV File Selected : {filename}")       


        except Exception as e:
                self.load_data_button.configure(state="Disabled")
                logger.error(f"Selecting CSV file Failed with error {str(e)}...")       
                messagebox.showerror("Error", "An error occurred - Selecting File")
 
    def load_file_data(self):
        logger.debug("Load Data Button Clicked")
        logger.info("Data Loading in progress...")
        
        # Retrieve the file path and header state
        path = self.path_entry.get().strip()
        header_state = self.no_headers_var.get()

        # Check if the path is empty
        if not path:
            messagebox.showerror("Error", "Please enter a file path or choose a file.")
            return

        # Attempt to read the data from the file
        try:
            result = read_data_with_header(path, header=header_state)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            logger.error(f"Failed to load file: {str(e)}")
            return

        # Check if the result is valid
        if result is None:
            messagebox.showerror("Error", "Failed to load the file.")
            return

        # Process data based on header state
        if header_state:
            logger.success("Data loaded without headers...")
            headers, data = result if result else ([], None)
        else:
            logger.success("Data loaded with headers...")
            data = result
            headers = data[0].keys() if data else []

        # Check if the data is empty
        if not data:
            messagebox.showwarning("Warning", "The file appears to be empty.")
            return

        # Update dropdowns with headers
        if headers:
            for label, dropdown in self.dropdowns:
                dropdown.configure(values=[""] + list(headers))
                dropdown.set("")
                
            self.header_dropdown.configure(values=[""] + list(headers))
            self.header_dropdown.set("")
            
        # Additional processing
        self.check_mandatory_fields()
        logger.success("Data successfully loaded.")

    def add_optional_field(self):
        field_name = self.optional_field_var.get()
        header_value = self.header_var.get()

        if field_name == "No optional field":
            messagebox.showwarning("Warning", "Please select an optional field.")
            return

        if header_value == "":
            messagebox.showwarning("Warning", "Please select a header value.")
            return

        if any(field[0] == field_name for field in self.optional_fields):
            messagebox.showwarning("Warning", "This optional field has already been added.")
            return
        


        index = len(self.optional_fields)
        row = index // 3
        col = (index % 3) * 2

        label = ctk.CTkLabel(self.optional_fields_container, text=f"{field_name}: {header_value}")
        label.grid(row=row, column=col, padx=5, pady=5, sticky="w")

        delete_button = ctk.CTkButton(self.optional_fields_container, text="X", width=30,
                                    command=lambda: self.delete_optional_field(field_name, label, delete_button))
        delete_button.grid(row=row, column=col + 1, padx=10, pady=5)

        self.optional_fields.append((field_name, header_value))

        current_options = list(self.optional_field_dropdown.cget("values"))
        current_options.remove(field_name)

        if len(current_options) == 1:
            current_options = ["No optional field"]
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(current_options) == 1 else current_options[1])

        self.header_dropdown.set("")

    def delete_optional_field(self, field_name, label, button):
        label.destroy()
        button.destroy()
        self.optional_fields = [field for field in self.optional_fields if field[0] != field_name]

        current_options = list(self.optional_field_dropdown.cget("values"))
        if "No optional field" not in current_options:
            current_options = ["No optional field"] + current_options
        current_options.append(field_name)
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(self.optional_fields) == 0 else current_options[1])

    def check_mandatory_fields(self, *args):
        # Check if all dropdowns have valid selections
        all_selected = all(
            dropdown.get().strip() not in ["No Column selected", "", " ", "- - - - - - - - - "] for _, dropdown in self.dropdowns
        )

        self.sync_button.configure(state="normal" if all_selected else "disabled")
        
    def Main_Process(self):
        
        global glob_vals
        template_ids = glob_vals
        
        header_state = self.no_headers_var.get()
        logger.info(f"Header State : {header_state}")
        
        file_path = self.path_entry.get()
        file_data = read_data_with_header(file_path,header_state)  
        
        print("\n --------------------- CSV FILE DATA-------------------- ",type(file_data))
        logger.debug(file_data)
        logger.info(f"CSV file readed Success")

            
            
        print("\n --------------------- SELECT FIELDS -------------------- ")
        mymappingdict={}
        
        for label, dropdown in self.dropdowns:
            if dropdown.get():
                mymappingdict[label]=dropdown.get()
            else:
                mymappingdict[label]="NOSELECTED"
                
        for name, header in self.optional_fields:
            mymappingdict[name]=header
            
        logger.debug(type(mymappingdict))
        logger.debug(mymappingdict)
        
        
        
        print("\n --------------------- GET DATA FROM SELECT FIELDS -------------------- ")
        data_rows=list()
        for row in file_data: # run on each row
            newdict=dict()
            for k,v in mymappingdict.items(): # run on eaych k,v
                newdict[k]=row.get(v,'ERROR')
                #print(k,v)
            data_rows.append(newdict)
            logger.debug(newdict)
            
        
        
        print("\n --------------------- VALIDATE DATA -------------------- ")

        for row in data_rows:  
            # ---------------------------------------------------------------------------------------------- COMPANY VALIDATION LIST ----------------------------------------------------------------------------------------------
            mylistc = []
            try:
                company_valid = Company_validation(**row)
                mylistc.append(company_valid.dict())
                
            except CompanyValidationError as e:
                error_message = str(e)
                response = self.custom_retry_continue_dialog(
                    "Company Data Validation", 
                    f" -------------- Validation failed --------------  \n \n  {error_message}\n\n Do you want to retry or continue?"
                )
                logger.error(f"Validation Error: {error_message}")
                
                if response == "exit":
                    return
                
            
                
            # ---------------------------------------------------------------------------------------------- CONSUMER VALIDATION LIST ----------------------------------------------------------------------------------------------
            mylistp = []       
            try:
                particpant_valid = Consumer_validation(**row)
                mylistp.append(particpant_valid.dict())
                
            except ConsumerValidationError as e:
                error_message = str(e)
                response = self.custom_retry_continue_dialog(
                    "Consumer Data Validation", 
                    f"-------------- Validation failed -------------- \n \n {error_message}\n\n Do you want to retry or continue?"
                )
                logger.error(f"Validation Error: {error_message}")
                
                if response == "exit":
                    return
                
                
# ----------------------------------------------------------------------------------------------TEST CONNECTION TO ZR  ----------------------------------------------------------------------------------------------
        print(f"\n ------------------------------ TEST CONNECTION TO ZR  ------------------------------ \n")
        zr_data['zr_ip'] = self.zr_ip.get().strip()
        zr_data['zr_port'] = self.zr_port.get().strip()
        zr_data['username'] = self.username.get().strip()
        zr_data['password'] = self.password.get().strip()
        
        logger.debug(zr_data)        
        
        test_zr_connection(zr_data)  
        print ("--------------------------------------------------------------------------------------------------------------- ")

# ---------------------------------------------------------------------------------------------- CONSUMER XML CONVERT  ----------------------------------------------------------------------------------------------
        print(f"\n ------------------------------ Company List :  ------------------------------ \n")
        logger.debug(f" Company List: \n {mylistc} \n")
        logger.info(f" Company List: {len(mylistc)}")
        
        print(f"\n ------------------------------ Participant List:  ------------------------------ \n")
        logger.debug(f"Participant List: \n {mylistp} \n")
        logger.info(f"Participant List:{len(mylistp)}")

        #print(" --------------------- XML OUTPUT DATA PARTICIPANT -------------------- \n")
        #for rowp in mylistp:
            #xml_data_part = consumer_to_xml(rowp)
            #logger.debug(xml_data_part)        
        
        
        #print(" --------------------- XML OUTPUT DATA COMPANY -------------------- \n")
        #for rowc in mylistc:
            #xml_data_comp = contract_to_xml(rowc)
            #logger.debug(xml_data_comp)  
        
        
# ---------------------------------------------------------------------------------------------- COMPANY IDS LIST ----------------------------------------------------------------------------------------------
        print("\n --------------------- EXTRACT COMPANY ID -------------------- ")
        company_ids = set(rowc.get('Company_id') for rowc in mylistc if rowc.get('Company_id'))
        logger.info(company_ids)
        print ("--------------------------------------------------------------------------------------------------------------- ")

        

# ----------------------------------------------------------------------------------------------  PROCESSING DATA & SEND REQUESTS ----------------------------------------------------------------------------------------------
        print("\n --------------------------  COMPANY's PROCESSING ---------------------------------------------------- ")
        for rowc in mylistc:
            company_id = rowc.get('Company_id')

            status_code, company_details = get_company_details(company_id)

             #comp found 
            if status_code != 404:
                logger.info(f"Company ID {company_id} found in the list of company's")
                logger.debug(company_details)
                
                id, name, _, _, _ = company_xml_parser(company_details)
                logger.debug(f"id: {id}")
                logger.debug(f"name: {name}")


            
            #comp not found 
            if status_code == 404:
                logger.info(f"Company ID {company_id} not found")
                                
                try:
                    xml_comp_data = contract_to_xml(rowc)
                    status_code, result = create_company(xml_comp_data)
                    logger.debug(f"Status code: {status_code}")
                    logger.debug(result)
                    
                    if status_code == 201:
                        logger.info(f"Company ID {company_id} created successfully --------------- ")
                    else:
                        logger.error(f"Failed to create Company ID {company_id}. Status code: {status_code}")
                except Exception as e:
                    logger.error(f"Error creating Company {company_id}: {e}")

        print ("--------------------------------------------------------------------------------------------------------------- ")




        print("\n --------------------------  PARTICPANT's PROCESSING ---------------------------------------------------- ")
        for rowp in mylistp:
            participant_id = rowp.get('Participant_Id')
            company_id = rowp.get('Company_id')
            
            status_code, participant_details = get_participant(company_id, participant_id)

            #comp found 
            if status_code != 404:
                logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                
            if status_code == 404:
                logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")

                ptcpt_type = rowp.get('Participant_Type', 3)
                if ptcpt_type == 2:
                    template_id = template_ids["season_parker"]
                if ptcpt_type == 6:
                    template_id = template_ids["pmvc"]
                if ptcpt_type == 6:
                    template_id = template_ids["cmp"]
                    
                    
                xml_ptcpt_data = consumer_to_xml(rowp)     
                logger.debug(xml_ptcpt_data)                
                status_code, result = create_participant(company_id, 3, xml_ptcpt_data)
                                            
                logger.info(f"Status code: {status_code}")
                logger.debug(f"Status code: {status_code}")
                logger.debug(result)
                print("\n")
                
                
                if status_code == 201:
                    logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                    
                if status_code == 500:
                    logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

        print ("--------------------------------------------------------------------------------------------------------------- ")

                    