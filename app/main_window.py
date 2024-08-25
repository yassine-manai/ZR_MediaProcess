import customtkinter as ctk
from tkinter import StringVar, filedialog, messagebox
from api.api_media import APIClient
from api.shift_api import ShiftPaymentAPIClient
from classes.error_except import CompanyValidationError, ConsumerValidationError
from functions.load_data import read_data_with_header
from classes.validator_class import Company_validation, Consumer_validation
from config.log_config import logger
from functions.dict_xml_user import consumer_to_xml, contract_to_xml
from functions.shift_dict_xml import close_shift_xml, open_shift_xml, topup_pmvc_xml
from functions.test_connect import test_zr_connection
from functions.xml_resp_parser import current_shift_response, get_status_code, open_shift_response
from globals.global_vars import configuration_data, glob_vals


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

mandatory_columns = [
    "Company_id", "Company_Name", "Company_ValidUntil", "Participant_Id",
    "Participant_Firstname", "Participant_Surname",
    "Participant_CardNumber","Participant_ValidUntil","Participant_ValidFrom", "Participant_LPN1"
]
optional_columns = [
    "Company_ValidFrom", "Company_Surname", "Company_phone1", "Company_email1", "Company_Street", "Company_Town",
    "Company_Postbox","Company_FilialId", "Participant_FilialId", "Participant_Type",
    "Participant_Cardclass", "Participant_IdentificationType",
    "Participant_Present", "Participant_Status", "Participant_GrpNo",
    "Participant_DisplayText", "Participant_LPN2", "Participant_LPN3", "Amount"
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
        
        self.cmp_label = ctk.CTkLabel(self, text="Proudly devloped by AsteroIdea © 2024 - V1.0"
                                ,text_color="white",corner_radius=8)
        
        self.cmp_label.grid(row=1, column=0, padx=10, pady=5, sticky="se")
        
        

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
        
                
        self.pmvc_var = ctk.BooleanVar(value=True)
        self.pmvc_var_check = ctk.CTkCheckBox(file_data_frame, text="PMVC Topup", variable=self.pmvc_var)
        self.pmvc_var_check.grid(row=0, column=5, padx=1, pady=5)

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data", command=self.load_file_data, state="disabled")
        self.load_data_button.grid(row=0, column=8, padx=1, pady=5)

        # Template ID section
        ctk.CTkLabel(file_data_frame, text="Template ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Season Parker ID
        ctk.CTkLabel(file_data_frame, text="Season Parker ID:").grid(row=1, column=1, padx=5, pady=5, sticky="e")
        self.template1_var = StringVar(value="2")
        self.template1_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template1_var, width=50)
        self.template1_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # PMVC ID
        ctk.CTkLabel(file_data_frame, text="PMVC ID:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        self.template2_var = StringVar(value="100")
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

    def update_date_format(self, selected_format):
        global glob_vals
        glob_vals['date_format_val'] = date_format_dict.get(selected_format, '%d-%m-%Y')
        logger.info(f"Date Format updated to: {glob_vals['date_format_val']}")

    def update_global_values(self):
        global glob_vals, configuration_data
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
        
        

        configuration_data['computer_id'] = self.computer_id.get()
        configuration_data['device_id'] = self.device_id.get()
        configuration_data['cashier_contract_id'] = self.cash_ctrt_id.get()
        configuration_data['cashier_consumer_id'] = self.cons_ctrt_id.get()
        
        configuration_data['zr_ip'] = self.zr_ip.get()
        configuration_data['zr_port'] = self.zr_port.get()
        configuration_data['username'] = self.zr_username.get()
        configuration_data['password'] = self.zr_password.get()
           
        logger.info(f"------------ {configuration_data}")
        
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

        self.sync_button = ctk.CTkButton(sync_frame, text="Sync", command=self.Main_Process, state="disabled", width=500, height=35)
        self.sync_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
  
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
        
        # ZR IP
        ctk.CTkLabel(footer_frame, text="ZR IP:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.zr_ip = ctk.CTkEntry(footer_frame)
        self.zr_ip.insert(0, "127.0.0.1")
        self.zr_ip.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # ZR Port
        ctk.CTkLabel(footer_frame, text="ZR PORT:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.zr_port = ctk.CTkEntry(footer_frame)
        self.zr_port.insert(0, "8000")
        self.zr_port.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        # ZR Username
        ctk.CTkLabel(footer_frame, text="ZR Username:").grid(row=0, column=4, padx=10, pady=5, sticky="w")
        self.zr_username = ctk.CTkEntry(footer_frame)
        self.zr_username.insert(0, "6")
        self.zr_username.grid(row=0, column=5, padx=10, pady=5, sticky="ew")

        # ZR Password
        ctk.CTkLabel(footer_frame, text="ZR Password:").grid(row=0, column=6, padx=10, pady=5, sticky="w")
        self.zr_password = ctk.CTkEntry(footer_frame)
        self.zr_password.insert(0, "4711")
        self.zr_password.grid(row=0, column=7, padx=10, pady=5, sticky="ew") 
                
    # SHIFTS DATA

        # computer_id
        ctk.CTkLabel(footer_frame, text="COMPUTER_ID:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.computer_id = ctk.CTkEntry(footer_frame)
        self.computer_id.insert(0, "7077")
        self.computer_id.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # device_id
        ctk.CTkLabel(footer_frame, text="Device ID:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.device_id = ctk.CTkEntry(footer_frame)
        self.device_id.insert(0, "799")
        self.device_id.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        # cash_ctrt_id
        ctk.CTkLabel(footer_frame, text="Cashier Contract ID:").grid(row=1, column=4, padx=10, pady=5, sticky="w")
        self.cash_ctrt_id = ctk.CTkEntry(footer_frame)
        self.cash_ctrt_id.insert(0, "1")
        self.cash_ctrt_id.grid(row=1, column=5, padx=10, pady=5, sticky="ew")

        # cons_ctrt_id
        ctk.CTkLabel(footer_frame, text="Cashier Consumer ID:").grid(row=1, column=6, padx=10, pady=5, sticky="w")
        self.cons_ctrt_id = ctk.CTkEntry(footer_frame)
        self.cons_ctrt_id.insert(0, "13")
        self.cons_ctrt_id.grid(row=1, column=7, padx=10, pady=5, sticky="ew")

        
        self.confirm_button = ctk.CTkButton(footer_frame, text="Test & Confirm", command=self.test_data, height=40)
        self.confirm_button.grid(row=0, column=8, rowspan=4, padx=5, pady=10, sticky="w")

     
        
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

        try:
            if header_state:
                logger.success("Data loaded without headers...")
                headers, data = result if result else ([], None)
            else:
                logger.success("Data loaded with headers...")
                data = result
                headers = data[0].keys() if data else []
        except Exception as e:
            logger.error(f"An error occurred while processing data: {e}")
            messagebox.showerror("Error", "Please enter a valid file path ")

            

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
        self.confirm_button.configure(state="normal" if all_selected else "disabled")

    def Main_Process(self):
        
        global glob_vals
        template_ids = glob_vals
        api_client = APIClient()
        shift_api = ShiftPaymentAPIClient()
        
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
        mylistc = []
        mylistp = []       

# --------------------------------------------------- COMPANY VALIDATION LIST ----------------------------------------------------------------------------------------------
        for row in data_rows: 
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
                

# ---------------------------------------------------------- CONSUMER VALIDATION LIST ----------------------------------------------------------------------------------------------
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
                
# ---------------------------------------------------------------- CONSUMER XML CONVERT  ----------------------------------------------------------------------------------------------
        print(f"\n ------------------------------ Company List :  ------------------------------ \n")
        logger.debug(f" Company List: \n {mylistc} \n")
        logger.info(f" Company List: {len(mylistc)}")
        
        print(f"\n ------------------------------ Participant List:  ------------------------------ \n")
        logger.debug(f"Participant List: \n {mylistp} \n")
        logger.info(f"Participant List:{len(mylistp)}")
        
        
# ----------------------------------------------------------------  PROCESSING DATA COMPANY & SEND REQUESTS ----------------------------------------------------------------------------------------------
       
        print("\n --------------------------  COMPANY's PROCESSING ---------------------------------------------------- ")
        for rowc in mylistc:
            print(rowc)
            
            company_id = rowc.get('Company_id')
            company_name = rowc.get('Company_Name')

            status_code, company_details = api_client.get_company_details(company_id)

            # Company found
            if status_code != 404:
                logger.info(f"Company ID {company_id} found in the list of companies")
                logger.debug(company_details)

                #id, name, _, _, _ = company_reponse_parser(company_details)
                #logger.debug(f"id: {id}")
                #logger.debug(f"name: {name}")


            # Company not found
            if status_code == 404:
                logger.info(f"Company ID {company_id} not found")
                try:
                    xml_comp_data = contract_to_xml(rowc)
                    status_code, result =  api_client.create_company(xml_comp_data)
                    logger.debug(f"Status code: {status_code}")
                    logger.debug(result)

                    if status_code == 201:
                        logger.info(f"Company ID {company_id} created successfully --------------- ")
                    else:
                        logger.error(f"Failed to create Company ID {company_id}. Status code: {status_code}")
                except Exception as e:
                    logger.error(f"Error creating Company {company_id}: {e}")
        print("--------------------------------------------------------------------------------------------------------------- ")

# ----------------------------------------------------------------  PROCESSING DATA PTCPT & SEND REQUESTS ----------------------------------------------------------------------------------------------
        specific_field_names = ["Amount", "Participant_Type"]
        missing_fields = [field for field in specific_field_names if not any(f[0] == field for f in self.optional_fields)]
        ptcpt_type_field = 'Participant_Type' if any(field[0] == 'Participant_Type' for field in self.optional_fields) else None
        Amount = 'Amount' if any(field[0] == 'Amount' for field in self.optional_fields) else None

        for rowp in mylistp:
            
            Participant_Type = rowp.get('Participant_Type')

            if not ptcpt_type_field:
                topup_value = self.pmvc_var.get()
                    
                if topup_value: 
                    messagebox.showwarning("Warning", f"The PMVC topup CheckBox is checked . \n Please add Participant Type or uncheck it.")

                if not topup_value: 
                    print("\n --------------------------  PARTICIPANT's PROCESSING -- NO PTCPT TYPE---------------------------------------------------- ")
                    participant_id = rowp.get('Participant_Id')
                    company_id = rowp.get('Company_id')
                    
                    
                    status_code, participant_details =  api_client.get_participant(company_id, participant_id)

                    # Participant found 
                    if status_code != 404:
                        logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")

                    # Participant not found   
                    if status_code == 404:
                        logger.info(f"******** Participant ID {participant_id} not found for Company ID {company_id}. ******** Creating new participant . . .")

                        template_id = template_ids["season_parker"]

                        print("********************************")
                        print(rowp)
                        print("********************************")
                        
                        xml_ptcpt_data = consumer_to_xml(rowp)
                        logger.debug(xml_ptcpt_data)                
                        status_code, result =  api_client.create_participant(company_id, template_id, xml_ptcpt_data)
                                                        
                        logger.info(f"Status code: {status_code}")
                        logger.debug(f"Status code: {status_code}")
                        logger.debug(result)
                        print("\n")
                        
                        if status_code == 201:
                            logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                            
                        if status_code == 500:
                            logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")
                
                        print("--------------------------------------------------------------------------------------------------------------- ")


            if ptcpt_type_field:
            
                
                if Participant_Type == 2:
                
                    print("\n --------------------------  PARTICIPANT's PROCESSING WITH PTCPT TYPE---------------------------------------------------- ")
                    participant_id = rowp.get('Participant_Id')
                    company_id = rowp.get('Company_id')
                    
                    
                    status_code, participant_details =  api_client.get_participant(company_id, participant_id)

                    # Participant found 
                    if status_code != 404:
                        logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")

                    # Participant not found   
                    if status_code == 404:
                        logger.info(f"******** Participant ID {participant_id} not found for Company ID {company_id}. ******** Creating new participant . . .")

                        template_id = template_ids["season_parker"]
                        
                        print("********************************")
                        print(rowp)
                        print("********************************")
                        
                        xml_ptcpt_data = consumer_to_xml(rowp)
                        logger.debug(xml_ptcpt_data)                
                        status_code, result =  api_client.create_participant(company_id, template_id, xml_ptcpt_data)
                                                        
                        logger.info(f"Status code: {status_code}")
                        logger.debug(f"Status code: {status_code}")
                        logger.debug(result)
                        print("\n")
                        
                        if status_code == 201:
                            logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                            
                        if status_code == 500:
                            logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")
                
                        print("--------------------------------------------------------------------------------------------------------------- ")
                    
                    
                if Participant_Type == 6:
                    
                    topup_value = self.pmvc_var.get()
                    
                    if topup_value: 
                        
                        logger.info(topup_value)
                        logger.success("TOPUP SELECTED . . . ")
                        
                        if not Amount:
                            messagebox.showwarning("Warning", f"The field Amount is missing. \n Please add it or uncheck the PMVC CheckBox.")
                            return
                        
                        if Amount:
                            
                            print("\n\n")
                            print("------------------ CURRENT SHIFT --------------------------------------------------------------------------------- ")
                            print("\n\n")

                            curr_status_code, curr_shift_detail =  shift_api.get_current_shift_api(1)
                            print(curr_shift_detail)
                            print(type(curr_shift_detail))
                            
                            stat = get_status_code(curr_shift_detail)

                            # If shift exists
                            if stat == 200 or stat ==201:
                                # Get Shift detail 
                                shift_status, shift_id, shift_no = current_shift_response(curr_shift_detail)
                                logger.info(f"SHIFT Status: {shift_status} -- SHIFT ID: {shift_id} -- SHIFT NO: {shift_no}")
                                logger.info(f"SHIFT ID: {shift_id} already Opened")
                                logger.debug(curr_shift_detail)
                                
                                participant_id = rowp.get('Participant_Id')
                                company_id = rowp.get('Company_id')
                                money_balance = rowp.get('Amount', 1)
                    

                                status_code, participant_details =  api_client.get_participant(company_id, participant_id)

                                # Participant found 
                                if status_code != 404:
                                    logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                                    
                                            
                                    print(participant_details)
                                    print(company_id)                            
                                    print(participant_id)
                                    print(money_balance)
                                    

                                    data = {
                                        "articles": [
                                            {
                                                "artClassRef": 0,
                                                "articleRef": 10624,
                                                "quantity": 1,
                                                "quantityExp": 0,
                                                "amount": 0,
                                                "influenceRevenue": 1,
                                                "influenceCashFlow": 1,
                                                "personalizedMoneyValueCard": {
                                                    "ContractId": company_id,
                                                    "ConsumerId": participant_id,
                                                    "addMoneyValue": int(money_balance)
                                                }
                                            }
                                        ]
                                    }
                                    
                                    print(f"------------------------------------ TOPUP for USER #{participant_id} -- Company {company_id}#------------------------------------------ ")
                                    
                                    # Topup PMVC
                                    print(data)
                                    data_topup_xml = topup_pmvc_xml(shift_id, data)
                                    print(data_topup_xml)
                                    status_code_tp, shift_detail = shift_api.topup_pmvc_api(shift_id, data_topup_xml)
                                    
                                    if status_code_tp == 200:
                                        logger.success("TOPUP successfully")
                                        logger.info("TOPUP successfully")
                                        logger.debug(shift_detail)
                                    
                                    if status_code_tp != 201:
                                        logger.error("ERROR !!!")
                                        logger.debug(shift_detail)
                                
                                # Participant not found   
                                if status_code == 404:
                                    logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")
                                    
                                    template_id = template_ids["pmvc"]

                                    print(rowp)
                                    xml_ptcpt_data = consumer_to_xml(rowp)
                                    logger.debug(xml_ptcpt_data)
                                    status_code, result = api_client.create_participant(company_id, template_id, xml_ptcpt_data)
                                    
                                    if status_code == 201:
                                        logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")

                                        data = {
                                            "articles": [
                                                {
                                                    "artClassRef": 0,
                                                    "articleRef": 10624,
                                                    "quantity": 1,
                                                    "quantityExp": 0,
                                                    "amount": 0,
                                                    "influenceRevenue": 1,
                                                    "influenceCashFlow": 1,
                                                    "personalizedMoneyValueCard": {
                                                        "ContractId": company_id,
                                                        "ConsumerId": participant_id,
                                                        "addMoneyValue": int(money_balance)
                                                    }
                                                }
                                            ]
                                        }
                                    
                                        print(f"------------------------------------ TOPUP for USER #{participant_id}#------------------------------------------ ")
                                        
                                        # Topup PMVC
                                        data_topup_xml = topup_pmvc_xml(shift_id, data)
                                        status_code_tp, shift_detail = shift_api.topup_pmvc_api(shift_id, data_topup_xml)
                                        
                                        if status_code_tp == 201:
                                            logger.success("TOPUP successfully")
                                            logger.info("TOPUP successfully")
                                            logger.debug(shift_detail)
                                        
                                        if status_code_tp != 201:
                                            logger.error("ERROR !!!")
                                            logger.debug(shift_detail)
                                        
                                        print("--------------------------------------------------------------------------------------------------------------- ")

                                    logger.info(f"Status code: {status_code}")
                                    logger.debug(f"Status code: {status_code}")
                                    logger.debug(result)
                                    print("\n")
                                    
                                    if status_code == 500:
                                        logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

            
                            # If shift does not exist
                            if stat == 500:
                                op_shift = open_shift_xml()
                                status_code, shift_detail = shift_api.open_shift_api(op_shift)
                                
                                if status_code == 200:
                                    logger.info("Opening Shift successful")
                                    logger.debug(f"Response {status_code} from Shift \n {shift_detail}")
                                    
                                    shift_status, shift_id, shift_no = open_shift_response(shift_detail)
                                    logger.info(f"SHIFT Status: {shift_status} -- SHIFT ID: {shift_id} -- SHIFT NO: {shift_no}")

                                    # Topup PMVC
                                    print("\n --------------------------  PARTICIPANT's PROCESSING ---------------------------------------------------- ")
                                    
                                    print(rowp)
                                    
                                    participant_id = rowp.get('Participant_Id')
                                    company_id = rowp.get('Company_id')
                                    money_balance = rowp.get('Amount', 0)
                                    
                                    status_code, participant_details =  api_client.get_participant(company_id, participant_id)

                                    # Participant found 
                                    if status_code != 404:
                                        logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")
                                                                
                                        template_id = template_ids["pmvc"]
    
                                        data = {
                                            "articles": [
                                                {
                                                    "artClassRef": 0,
                                                    "articleRef": 10624,
                                                    "quantity": 1,
                                                    "quantityExp": 0,
                                                    "amount": 0,
                                                    "influenceRevenue": 1,
                                                    "influenceCashFlow": 1,
                                                    "personalizedMoneyValueCard": {
                                                        "ContractId": company_id,
                                                        "ConsumerId": participant_id,
                                                        "addMoneyValue": int(money_balance)
                                                    }
                                                }
                                            ]
                                        }
                                    
                                        print(f"------------------------------------ TOPUP for USER #{participant_id}#------------------------------------------ ")
                                        
                                        # Topup PMVC
                                        data_topup_xml = topup_pmvc_xml(shift_id, data)
                                        status_code_tp, shift_detail = shift_api.topup_pmvc_api(shift_id, data_topup_xml)
                                        
                                        if status_code_tp == 200:
                                            logger.success("TOPUP successfully")
                                            logger.info("TOPUP successfully")
                                            logger.debug(shift_detail)
                                        
                                        if status_code_tp != 201:
                                            logger.error("ERROR !!!")
                                            logger.debug(shift_detail)

                                    # Participant not found   
                                    if status_code == 404:
                                        logger.info(f"Participant ID {participant_id} not found for Company ID {company_id}. Creating new participant . . .")

                                        template_id = template_ids["pmvc"]

                                        print(rowp)
                                        
                                        xml_ptcpt_data = consumer_to_xml(rowp)
                                        logger.debug(xml_ptcpt_data)
                                        status_code, result = api_client.create_participant(company_id, template_id, xml_ptcpt_data)
                                        
                                        if status_code == 201:
                                            logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")

                                            data = {
                                                "articles": [
                                                    {
                                                        "artClassRef": 0,
                                                        "articleRef": 10624,
                                                        "quantity": 1,
                                                        "quantityExp": 0,
                                                        "amount": 0,
                                                        "influenceRevenue": 1,
                                                        "influenceCashFlow": 1,
                                                        "personalizedMoneyValueCard": {
                                                            "ContractId": company_id,
                                                            "ConsumerId": participant_id,
                                                            "addMoneyValue": int(money_balance)
                                                        }
                                                    }
                                                ]
                                            }
                                    
                                            print(f"------------------------------------ TOPUP for USER #{participant_id}#------------------------------------------ ")
                                            
                                            # Topup PMVC
                                            data_topup_xml = topup_pmvc_xml(shift_id, data)
                                            status_code_tp, shift_detail = shift_api.topup_pmvc_api(shift_id, data_topup_xml)
                                            
                                            if status_code_tp == 200:
                                                logger.success("TOPUP successfully")
                                                logger.info("TOPUP successfully")
                                                logger.debug(shift_detail)
                                            
                                            if status_code_tp != 201:
                                                logger.error("ERROR !!!")
                                                logger.debug(shift_detail)
                                                
                                                print("--------------------------------------------------------------------------------------------------------------- ")

                                            logger.info(f"Status code: {status_code}")
                                            logger.debug(f"Status code: {status_code}")
                                            logger.debug(result)
                                            print("\n")
                                        
                                        if status_code == 500:
                                            logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

                    if not topup_value:     
                            
                            participant_id = rowp.get('Participant_Id')
                            company_id = rowp.get('Company_id')
                            
                            
                            status_code, participant_details =  api_client.get_participant(company_id, participant_id)

                            # Participant found 
                            if status_code != 404:
                                logger.info(f"Participant ID {participant_id} found for Company ID {company_id}")

                            # Participant not found   
                            if status_code == 404:
                                logger.info(f"******** Participant ID {participant_id} not found for Company ID {company_id}. ******** Creating new participant . . .")

                                template_id = template_ids["pmvc"]
                                
                                print("********************************")
                                print(rowp)
                                print("********************************")
                                
                                xml_ptcpt_data = consumer_to_xml(rowp)
                                logger.debug(xml_ptcpt_data)                
                                status_code, result =  api_client.create_participant(company_id, template_id, xml_ptcpt_data)
                                                                
                                logger.info(f"Status code: {status_code}")
                                logger.debug(f"Status code: {status_code}")
                                logger.debug(result)
                                print("\n")
                                
                                if status_code == 201:
                                    logger.info(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                                    
                                if status_code == 500:
                                    logger.error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")
                        
                                print("--------------------------------------------------------------------------------------------------------------- ")
           
                                    
                            
                    
        # Close SHIFT
        data_close = close_shift_xml(shift_id, shift_status)
        status_code, shift_detail = shift_api.close_shift_api(shift_id, data_close)

        if status_code == 200:
            logger.info(f"Close Shift for Shift ID {shift_id} successful")
            logger.debug(f"Response {status_code} from Shift {shift_detail}")
            
        else:
            logger.error(f"Error Occurred while closing Shift ID {shift_id}")
            logger.debug(f"Response {status_code} from Shift {shift_detail}")
    
                    

                    
    def test_data(self):
        print("Test data")
        
        print("\n --------------------- UPDATE GLOBAL VALS -------------------- ")
        self.update_global_values()
        
        print(f"\n ------------------------------ TEST CONNECTION TO ZR  ------------------------------ \n")
        
        #logger.debug(zr_data)   
        
        print("\n --------------------- TEST ZR -------------------- ")
        test_zr_connection()        
        
