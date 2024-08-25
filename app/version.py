from threading import Thread
import time
import tkinter as tk
from tkinter import StringVar, filedialog, messagebox
import customtkinter as ctk
from PIL import Image
from config.log_config import logger
from functions.test_connect import test_zr_connection
from globals.global_vars import zr_data, glob_vals, configuration_data
from functions.load_data import read_data_with_header

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")
        

class Version2(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PAYG Import Tool™️")
        self.geometry("1300x740")
        self.resizable(False, False)

        self.date_format_dict = {
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
        self.mandatory_columns = [
            "Company_id", "Company_Name", "Company_ValidUntil", "Participant_Id",
            "Participant_Firstname", "Participant_Surname","Participant_CardNumber",
            "Participant_ValidUntil","Participant_ValidFrom", 
        ]
        self.optional_columns = [
            "Company_ValidFrom", "Company_Surname", "Company_phone1", "Company_email1",
            "Company_Street", "Company_Town","Company_Postbox","Company_FilialId", 
            "Participant_FilialId", "Participant_Type","Participant_Cardclass", 
            "Participant_IdentificationType","Participant_Present", "Participant_Status", 
            "Participant_GrpNo","Participant_DisplayText","Participant_LPN1", 
            "Participant_LPN2", "Participant_LPN3", "Amount"
        ]
        
       
        self.optional_field_count = 0
        self.optional_fields = []
        
        logger.info("Starting UI in progress . . .")

        self.setup_ui()
        self.after(100, self.open_configuration)
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.create_title_frame()
        self.create_main_frame()
        self.create_footer_frame()
    def custom_error_dialog(self, title, message):
        dialog = ctk.CTkToplevel()
        dialog.title(title)
        dialog.geometry("500x140")
        
        def on_exit():
            dialog.destroy()
        
        ctk.CTkLabel(dialog, text=message, wraplength=400).pack(pady=10)
        exit_button = ctk.CTkButton(dialog, text="Exit", command=on_exit)
        exit_button.pack(pady=20)

        dialog.grab_set()
        dialog.wait_window()




# ------------------------------------- Titile Frame ----------------------------------------------------
    def create_title_frame(self):
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            title_frame,
            text="PAYG Import Tool",
            font=("Arial", 24, "bold"),
            text_color="white",
            corner_radius=8
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            title_frame,
            text="  Configuration ",
            text_color="black",
            width=30,
            height=30,
            fg_color="white",
            hover_color=("gray70", "gray30"),
            command=self.open_configuration
        ).grid(row=0, column=2, sticky="e", padx=(0, 10))

# ------------------------------------- Titile Frame - Compns ----------------------------------------------------
    def open_configuration(self):
        if hasattr(self, 'config_window') and self.config_window.winfo_exists():
            self.config_window.lift()
            return

        logger.info(f"Configuration Popup opened")

        self.create_blurred_overlay()

        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuration")
        self.config_window.geometry("400x390")
        self.config_window.resizable(True, True)

        # Center the config window
        self.center_window(self.config_window)
                
        self.create_zr_config()
        self.create_shift_config()

        # Load saved data
        self.load_configuration_data()

        save_button = ctk.CTkButton(self.config_window, text="Save", command=self.save_configuration, width=200)
        save_button.grid(row=10, column=1, columnspan=2, pady=20)
        
        # Make the configuration window modal
        self.config_window.transient(self)
        self.config_window.grab_set()
        self.config_window.protocol("WM_DELETE_WINDOW", self.on_config_close)
        self.wait_window(self.config_window)

    def on_config_close(self):
        self.overlay.destroy()
        self.config_window.destroy()
        logger.info("Configuration popup closed")

    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
                    
    def create_zr_config(self):
        ctk.CTkLabel(self.config_window, text="ZR Infos", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.config_window, text="ZR IP:").grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.zr_ip_entry = ctk.CTkEntry(self.config_window)
        self.zr_ip_entry.insert(0, "0")
        self.zr_ip_entry.grid(row=6, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="ZR PORT:").grid(row=7, column=1, padx=10, pady=5, sticky="w")
        self.zr_port_entry = ctk.CTkEntry(self.config_window)
        self.zr_port_entry.insert(0, "0")
        self.zr_port_entry.grid(row=7, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="ZR Username:").grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.zr_username_entry = ctk.CTkEntry(self.config_window)
        self.zr_username_entry.insert(0, "0")
        self.zr_username_entry.grid(row=8, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="ZR Password:").grid(row=9, column=1, padx=10, pady=5, sticky="w")
        self.zr_password_entry = ctk.CTkEntry(self.config_window)
        self.zr_password_entry.insert(0, "0")
        self.zr_password_entry.grid(row=9, column=2, padx=10, pady=5)

    def create_shift_config(self):
        ctk.CTkLabel(self.config_window, text="SHIFT Infos", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.config_window, text="Computer ID:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.computer_id_entry = ctk.CTkEntry(self.config_window)
        self.computer_id_entry.insert(0, "0")
        self.computer_id_entry.grid(row=1, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="Device ID:").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.device_id_entry = ctk.CTkEntry(self.config_window)
        self.device_id_entry.insert(0, "0")
        self.device_id_entry.grid(row=2, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="Cashier Contract ID:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.cashier_contract_id_entry = ctk.CTkEntry(self.config_window)
        self.cashier_contract_id_entry.insert(0, "0")
        self.cashier_contract_id_entry.grid(row=3, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="Cashier Consumer ID:").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.cashier_consumer_id_entry = ctk.CTkEntry(self.config_window)
        self.cashier_consumer_id_entry.insert(0, "0")
        self.cashier_consumer_id_entry.grid(row=4, column=2, padx=10, pady=5)

    def save_configuration(self):
        global configuration_data

        configuration_data['computer_id'] = self.computer_id_entry.get().strip()
        configuration_data['device_id'] = self.device_id_entry.get().strip()
        configuration_data['cashier_contract_id'] = self.cashier_contract_id_entry.get().strip()
        configuration_data['cashier_consumer_id'] = self.cashier_consumer_id_entry.get().strip()

        configuration_data['zr_ip'] = self.zr_ip_entry.get().strip()
        configuration_data['zr_port'] = self.zr_port_entry.get().strip()
        configuration_data['username'] = self.zr_username_entry.get().strip()
        configuration_data['password'] = self.zr_password_entry.get().strip()

        logger.info(f"Configuration Saved: \n {configuration_data}")
        self.overlay.destroy()
        self.config_window.destroy()

    def create_blurred_overlay(self):
        self.overlay = ctk.CTkFrame(self, fg_color="gray26")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.configure(corner_radius=0)

    def load_configuration_data(self):
        global configuration_data
        self.computer_id_entry.delete(0, 'end')
        self.computer_id_entry.insert(0, configuration_data['computer_id'])
        
        self.device_id_entry.delete(0, 'end')
        self.device_id_entry.insert(0, configuration_data['device_id'])
        
        self.cashier_contract_id_entry.delete(0, 'end')
        self.cashier_contract_id_entry.insert(0, configuration_data['cashier_contract_id'])
        
        self.cashier_consumer_id_entry.delete(0, 'end')
        self.cashier_consumer_id_entry.insert(0, configuration_data['cashier_consumer_id'])
        
        self.zr_ip_entry.delete(0, 'end')
        self.zr_ip_entry.insert(0, configuration_data['zr_ip'])
        
        self.zr_port_entry.delete(0, 'end')
        self.zr_port_entry.insert(0, configuration_data['zr_port'])
        
        self.zr_username_entry.delete(0, 'end')
        self.zr_username_entry.insert(0, configuration_data['username'])
        
        self.zr_password_entry.delete(0, 'end')
        self.zr_password_entry.insert(0, configuration_data['password'])







# ------------------------------------- Main Frame ----------------------------------------------------
    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.create_file_input_frame(main_frame)
        self.create_mandatory_fields_frame(main_frame)
        self.create_optional_fields_frame(main_frame)
        self.create_button_frame(main_frame)
# -----------------------------------------------------------------------------------------------------
    
     
# ------------------------------------- Main Frame - Compns - Data input  -----------------------------
    def create_file_input_frame(self, parent):
        file_data_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        file_data_frame.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="new")
        file_data_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        ctk.CTkLabel(file_data_frame, text="CSV file Selection", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=10, padx=10, pady=(10, 10), sticky="news")

        ctk.CTkLabel(file_data_frame, text="File Path:", font=("Arial", 15)).grid(row=1, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
        self.path_entry = ctk.CTkEntry(file_data_frame, width=600)
        self.path_entry.grid(row=1, column=1, columnspan=6, padx=5, pady=(5, 5), sticky="w")
        self.path_entry.bind("<KeyRelease>", self.update_load_button_state)

        ctk.CTkButton(file_data_frame, text="Browse", command=self.browse_file).grid(row=1, column=7, padx=5, pady=(5, 5))

        self.no_headers_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(file_data_frame, text="No Headers", variable=self.no_headers_var).grid(row=1, column=8, padx=5, pady=(5, 5))

        self.pmvc_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(file_data_frame, text="PMVC Topup", variable=self.pmvc_var).grid(row=1, column=9, padx=5, pady=(5, 5))

        # Template ID section
        ctk.CTkLabel(file_data_frame, text="Template ID:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="w")

        # Season Parker ID
        ctk.CTkLabel(file_data_frame, text="Season Parker ID:").grid(row=2, column=1, padx=5,  pady=5, sticky="e")
        self.template1_var = StringVar(value="2")
        self.template1_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template1_var, width=50)
        self.template1_entry.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        # PMVC ID
        ctk.CTkLabel(file_data_frame, text="PMVC ID:").grid(row=2, column=3, padx=5, pady=5, sticky="e")
        self.template2_var = StringVar(value="100")
        self.template2_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template2_var, width=50)
        self.template2_entry.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

        # CPM ID
        ctk.CTkLabel(file_data_frame, text="CPM ID:").grid(row=2, column=5, padx=5, pady=5, sticky="e")
        self.template3_var = StringVar(value="3")
        self.template3_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template3_var, width=50)
        self.template3_entry.grid(row=2, column=6, padx=5, pady=5, sticky="ew")
        

        ctk.CTkLabel(file_data_frame, text="Date Format:").grid(row=2, column=7, padx=5, pady=(5, 5), sticky="e")
        self.date_format_var = StringVar(value="yyyy-mm-dd")
        ctk.CTkOptionMenu(file_data_frame, variable=self.date_format_var, values=list(self.date_format_dict.keys()), width=150, command=self.update_date_format).grid(row=2, column=8, columnspan=2, padx=5, pady=5, sticky="w")

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data", command=self.load_file_data, state="disabled")
        self.load_data_button.grid(row=3, column=0, columnspan=10, padx=10, pady=(15, 10), sticky="ew")

    def update_date_format(self, selected_format):
        global glob_vals
        glob_vals['date_format_val'] = self.date_format_dict.get(selected_format, '%d-%m-%Y')
        logger.info(f"Date Format updated to: {glob_vals['date_format_val']}")

    def update_global_values(self):
        global glob_vals
        selected_format = self.date_format_var.get()
        glob_vals['date_format_val'] = self.date_format_dict.get(selected_format, '%d-%m-%Y')
        glob_vals['season_parker'] = self.template1_var.get()
        glob_vals['pmvc'] = self.template2_var.get()
        glob_vals['cmp'] = self.template3_var.get()
        
        pmvc = self.pmvc_var.get()
        header = self.no_headers_var.get()
        
        template_id1 = int(glob_vals['season_parker'])
        template_id2 = int(glob_vals['pmvc'])
        template_id3 = int(glob_vals['cmp'])
        logger.info(f"------------ {glob_vals['date_format_val']}")
        
        logger.info(f"Template IDs updated to: {template_id1} -- {template_id2} -- {template_id3}") 
        logger.info(f"Checkboxes updated to:  Headers {header} -- PMVC topup {pmvc}") 
        logger.info(f"Date format selected : {selected_format}") 

    def update_load_button_state(self, event=None):
        path = self.path_entry.get().strip()
        self.load_data_button.configure(state="normal" if path else "disabled")

    def browse_file(self):
        logger.debug("Selecting file process started...")
        try:
            filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if filename:
                self.path_entry.delete(0, ctk.END)
                self.path_entry.insert(0, filename)
                self.load_data_button.configure(state="normal")
                logger.success(f"CSV File Selected: {filename}")
        except Exception as e:
            self.load_data_button.configure(state="disabled")
            logger.error(f"Selecting CSV file Failed with error {str(e)}...")
            messagebox.showerror("Error", "An error occurred - Selecting File")

    def load_file_data(self):
        logger.debug("Load Data Button Clicked")
        logger.info("Data Loading in progress...")

        path = self.path_entry.get().strip()
        header_state = self.no_headers_var.get()

        if not path:
            self.custom_error_dialog("Error", "Please enter a file path or choose a file.")
            return

        try:
            result = read_data_with_header(path, header=header_state)
            if result is None:
                self.custom_error_dialog("Error", "Failed to load the file.")
                return

            if header_state:
                logger.success("Data loaded without headers...")
                headers, data = result if result else ([], None)
            else:
                logger.success("Data loaded with headers...")

                data = result
                headers = data[0].keys() if data else []

            if not data:
                self.custom_error_dialog("Warning", "The file appears to be empty.")
                return

            if headers:
                for label, dropdown in self.dropdowns:
                    dropdown.configure(values=[""] + list(headers))
                    dropdown.set("")

                self.header_dropdown.configure(values=[""] + list(headers))
                self.header_dropdown.set("")

            self.check_mandatory_fields()
            self.update_global_values()
            #self.custom_error_dialog("Sucsess", "Data loaded successfully")
            self.on_data_loaded("success")
            logger.success("Data successfully loaded.")


        except Exception as e:
            logger.error(f"An error occurred while processing data: {e}")
            self.custom_error_dialog("Error", f"An error occurred:  Please Check your file data \n {str(e)}")
            self.on_data_loaded("error")

# ----------------------------------------------------------------------------------------------------------

    



# ------------------------------------- Main Frame - Compns - madatory fild  --------------------------------

    def create_mandatory_fields_frame(self, parent):
        mandatory_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        mandatory_frame.grid(row=0, column=0, padx=10, pady=(200, 40), sticky="new")
        mandatory_frame.grid_columnconfigure((1, 3, 5, 7, 9), weight=1)

        ctk.CTkLabel(mandatory_frame, text="Mandatory Fields Selections", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=10, padx=10, pady=(10, 10), sticky="news")
       
        # Create the status icon label
        self.status_label = ctk.CTkLabel(mandatory_frame, text="Loading...", font=("Arial", 18, "bold"))
        self.status_label.grid(row=0, column=7, padx=10, pady=(10, 10), sticky="e")
        
        
        self.dropdowns = []
        for i, label in enumerate(self.mandatory_columns):
            row = (i // 4) + 1
            col = (i % 4) * 2

            ctk.CTkLabel(mandatory_frame, text=label).grid(row=row, column=col, padx=10, pady=10, sticky="news")
            dropdown = ctk.CTkOptionMenu(mandatory_frame, width=150, values="", command=self.check_mandatory_fields)
            dropdown.grid(row=row, column=col+1, padx=10, pady=10, sticky="news")
            dropdown.set("- - - - - - - - -")
            self.dropdowns.append((label, dropdown))
    
    def on_data_loaded(self, status):
    # Update the status label to show success when data is loaded
        if status == "success":
            self.status_label.configure(text="✔ Data Loaded", text_color="green")
            
        if status == "error":
            self.status_label.configure(text="✘ Error", text_color="red")
    
    def check_mandatory_fields(self, *args):
        all_selected = all(
            dropdown.get().strip() not in ["", "No Column selected", "- - - - - - - - -"]
            for _, dropdown in self.dropdowns
        )
        
        # The status icon in this function is unrelated to data load status
        self.button1.configure(state="normal" if all_selected else "disabled")
# ------------------------------------------------------------------------------------------------------------



# ------------------------------------- Main Frame - Compns - optional fild  -----------------------------------
    def create_optional_fields_frame(self, parent):
        self.optional_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        self.optional_frame.grid(row=0, column=0, padx=10, pady=(410, 40), sticky="new")
        self.optional_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self.optional_frame, text="Optional Fields Selections", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=4, pady=(10,20))

        # Field label and dropdown
        ctk.CTkLabel(self.optional_frame, text="Field:",anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
        self.optional_field_var = StringVar()
        self.optional_field_dropdown = ctk.CTkOptionMenu(self.optional_frame, variable=self.optional_field_var, values=["No optional field"] + self.optional_columns, width=200)
        self.optional_field_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="nw")
        self.optional_field_dropdown.set("No optional field")

        # Header label and dropdown
        ctk.CTkLabel(self.optional_frame, text="Header:",anchor="w").grid(row=1, column=2, padx=5, pady=5, sticky="nw")
        self.header_var = StringVar()
        self.header_dropdown = ctk.CTkOptionMenu(self.optional_frame, variable=self.header_var, values=[""], width=200)
        self.header_dropdown.grid(row=1, column=3, padx=5, pady=5, sticky="nw")
        self.header_dropdown.set("No Column selected")

        # Add button
        ctk.CTkButton(self.optional_frame, text="+", width=30, command=self.add_optional_field).grid(row=1, column=4, padx=5, pady=5, sticky="nw")

        self.optional_fields_container = ctk.CTkFrame(self.optional_frame, fg_color="transparent")
        self.optional_fields_container.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.optional_fields_container.grid_columnconfigure(0, weight=1)
        
        # Set an initial height for the container
        self.optional_fields_container.configure(height=20)  

        self.optional_fields = []

    def add_optional_field(self):
        field_name = self.optional_field_var.get()
        header_value = self.header_var.get()

        if field_name == "No optional field":
            self.custom_error_dialog("Error", "Please select an optional field.")
            return

        if header_value == "":
            self.custom_error_dialog("Error", "Please select a header value .")
            return

        if any(field[0] == field_name for field in self.optional_fields):
            self.custom_error_dialog("Error", "This optional field has already been added.")
            return            


        frame = ctk.CTkFrame(self.optional_fields_container)
        frame.pack(fill="x", padx=5, pady=2)

        label_frame = ctk.CTkFrame(frame, fg_color="transparent")
        label_frame.pack(side="left", fill="x", expand=True)

        label = ctk.CTkLabel(label_frame, text=f"{field_name}: {header_value}", anchor="w")
        label.pack(side="left", padx=5, fill="x", expand=True)

        delete_button = ctk.CTkButton(label_frame, text="X", width=30,
                                    command=lambda: self.delete_optional_field(field_name, frame))
        delete_button.pack(side="right", padx=5)

        self.optional_fields.append((field_name, header_value, frame))

        current_options = list(self.optional_field_dropdown.cget("values"))
        current_options.remove(field_name)

        if len(current_options) == 1:
            current_options = ["No optional field"]
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(current_options) == 1 else current_options[1])

        self.header_dropdown.set("")
        self.update_frame_size()    
        
    def delete_optional_field(self, field_name, frame):
        frame.destroy()
        self.optional_fields = [field for field in self.optional_fields if field[0] != field_name]

        current_options = list(self.optional_field_dropdown.cget("values"))
        if "No optional field" not in current_options:
            current_options = ["No optional field"] + current_options
        current_options.append(field_name)
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set("No optional field" if len(self.optional_fields) == 0 else current_options[1])

        self.update_frame_size()

    def update_frame_size(self):
        if self.optional_fields:
            total_height = sum(frame.winfo_reqheight() for _, _, frame in self.optional_fields)
            self.optional_fields_container.configure(height=max(30, total_height))  
        else:
            self.optional_fields_container.configure(height=30) 
        self.optional_frame.update_idletasks()

# ---------------------------------------------------------------------------------------------------------------

    
    
    
# ------------------------------------- Main Frame - Compns - Button process fild  ------------------------------
    def create_button_frame(self, parent):
        button_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        button_frame.grid(row=0, column=0, padx=10, pady=(550, 40), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Button 1
        self.button1 = ctk.CTkButton(button_frame, text="Data validation", command=lambda: self.button_action(1))
        self.button1.grid(row=0, column=0, padx=5, pady=20)

        # Button 2
        self.button2 = ctk.CTkButton(button_frame, text="Check ZR connection", command=lambda: self.button_action(2), state="disabled")
        self.button2.grid(row=0, column=1, padx=5, pady=20)
        
        # Button 3
        self.button3 = ctk.CTkButton(button_frame, text="Start Process", command=lambda: self.button_action(3), state="disabled")
        self.button3.grid(row=0, column=2, padx=5, pady=20)

    def button_action(self, button_number):
        # Reset all button texts
        self.reset_button_texts()

        # Start the loading animation in a separate thread
        Thread(target=self.run_loading_animation, args=(button_number,)).start()

    def run_loading_animation(self, button_number):
        # Select the correct button and perform specific actions
        if button_number == 1:
            button = self.button1
        elif button_number == 2:
            button = self.button2
        else:
            button = self.button3

        # Show loading text/icon
        button.configure(text=f"{button.cget('text')} ⏳")

        # Simulate test result
        test_result = self.simulate_test(button_number)

        # Update the button text based on the test result
        if test_result == 1:
            button.configure(text="Checking Success ✔️")
            logger.info(f"Button {button_number} action succeeded")
            
            if button_number == 1:
                self.button1.configure(state="disabled")
                self.button2.configure(state="normal")  # Enable button 2 if the test succeeds
            elif button_number == 2:
                self.button2.configure(state="disabled")
                self.button3.configure(state="normal")  # Enable button 3 if ZR connection check succeeds
        else:
            button.configure(text="Error ❌")
            logger.error(f"Button {button_number} action failed")
            self.reset_button_texts()
            self.reset_button_states()

    def simulate_test(self, button_number):
        # Simulate a delay
        time.sleep(2)

        if button_number == 1:
            # Simulate data validation
            return 1  # Always succeed for this example
        elif button_number == 2:
            # Use the actual test_zr_connection function
            print("\n ------------------------------ TEST CONNECTION TO ZR  ------------------------------ \n")
            logger.debug(zr_data)
            zr = test_zr_connection()
            
            # Determine the status of the connection
            if zr == 200:
                logger.info("Test connection established")
                self.code_stat = True 
                return 1
            elif zr == 404:
                logger.info("Error: Test connection failed")
                self.code_stat = False  
                return 0
            
            print("----------------------------------------------------------------------------------------- ")
        else:
            return 0  # Simulate failure for button 3

    def reset_button_texts(self):
        # Reset all button texts to their original state
        self.button1.configure(text="Data validation")
        self.button2.configure(text="Check ZR connection")
        self.button3.configure(text="Start Process")

    def reset_button_states(self):
        # Reset all button states to their original state
        self.button1.configure(state="normal")
        self.button2.configure(state="disabled")
        self.button3.configure(state="disabled")
# -----------------------------------------------------------------------------------------------------------------
        

    
    
    
    
    
    
    
    
# ----------------------------------------------------------- Footer Frame -----------------------------------------
    def create_footer_frame(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(footer_frame, text="Version 2.0", text_color="white", corner_radius=8).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(footer_frame, text="AsteroIdea © 2024", text_color="white", corner_radius=8).grid(row=0, column=0, sticky="e")    
# ------------------------------------------------------------------------------------------------------------------
