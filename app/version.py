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
        self.title("PAYG Import Tool")
        self.geometry("1300x700")
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
            "Participant_Firstname", "Participant_Surname",
            "Participant_CardNumber", "Participant_LPN1"
        ]
        self.optional_columns = [
            "Company_ValidFrom", "Company_Surname", "Company_phone1", "Company_email1",
            "Company_Street", "Company_Town", "Company_Postbox", "Company_FilialId",
            "Participant_FilialId", "Participant_Type", "Participant_Cardclass",
            "Participant_IdentificationType", "Participant_ValidFrom", "Participant_ValidUntil",
            "Participant_Present", "Participant_Status", "Participant_GrpNo",
            "Participant_DisplayText", "Participant_LPN2", "Participant_LPN3", "Money_Balance"
        ]

        self.optional_field_count = 0
        self.optional_fields = []

        self.setup_ui()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.create_title_frame()
        self.create_main_frame()
        self.create_footer_frame()

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

        config_icon = ctk.CTkImage(light_image=Image.open("./assets/settings.png"), size=(24, 24))
        ctk.CTkButton(
            title_frame,
            image=config_icon,
            text="Configuration ",
            text_color="black",
            width=30,
            height=30,
            fg_color="white",
            hover_color=("gray70", "gray30"),
            command=self.open_configuration
        ).grid(row=0, column=2, sticky="e", padx=(0, 10))

    def create_main_frame(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.create_file_input_frame(main_frame)
        self.create_mandatory_fields_frame(main_frame)
        self.create_optional_fields_frame(main_frame)
        self.create_button_frame(main_frame)

    def create_file_input_frame(self, parent):
        file_data_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        file_data_frame.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="new")
        file_data_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        ctk.CTkLabel(file_data_frame, text="CSV file Section", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=10, padx=10, pady=(10, 10), sticky="news")

        ctk.CTkLabel(file_data_frame, text="File Path:", font=("Arial", 15)).grid(row=1, column=0, padx=(10, 5), pady=(5, 5), sticky="w")
        self.path_entry = ctk.CTkEntry(file_data_frame, width=600)
        self.path_entry.grid(row=1, column=1, columnspan=6, padx=5, pady=(5, 5), sticky="w")
        self.path_entry.bind("<KeyRelease>", self.update_load_button_state)

        ctk.CTkButton(file_data_frame, text="Browse", command=self.browse_file).grid(row=1, column=7, padx=5, pady=(5, 5))

        self.no_headers_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(file_data_frame, text="No Headers", variable=self.no_headers_var).grid(row=1, column=8, padx=5, pady=(5, 5))

        self.pmvc_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(file_data_frame, text="PMVC Topup", variable=self.pmvc_var).grid(row=1, column=9, padx=5, pady=(5, 5))

        # Template ID section
        ctk.CTkLabel(file_data_frame, text="Template ID:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="w")

        template_ids = [
            ("Season Parker ID:", "1"),
            ("PMVC ID:", "2"),
            ("CPM ID:", "3")
        ]

        for i, (label, default_value) in enumerate(template_ids):
            ctk.CTkLabel(file_data_frame, text=label).grid(row=2, column=2*i+1, padx=5, pady=(5, 5), sticky="e")
            var = StringVar(value=default_value)
            ctk.CTkEntry(file_data_frame, textvariable=var, width=80).grid(row=2, column=2*i+2, padx=5, pady=(5, 5), sticky="w")

        ctk.CTkLabel(file_data_frame, text="Date Format:").grid(row=2, column=7, padx=5, pady=(5, 5), sticky="e")
        self.date_format_var = StringVar(value="yyyy-mm-dd")
        ctk.CTkOptionMenu(file_data_frame, variable=self.date_format_var, values=list(self.date_format_dict.keys()), width=150).grid(row=2, column=8, columnspan=2, padx=5, pady=(5, 5), sticky="w")

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data", command=self.load_file_data, state="disabled")
        self.load_data_button.grid(row=3, column=0, columnspan=10, padx=10, pady=(15, 10), sticky="ew")

    def create_mandatory_fields_frame(self, parent):
        mandatory_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        mandatory_frame.grid(row=0, column=0, padx=10, pady=(210, 40), sticky="new")
        mandatory_frame.grid_columnconfigure((1, 3, 5, 7, 9), weight=1)

        ctk.CTkLabel(mandatory_frame, text="Mandatory Fields Selections", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=10, padx=10, pady=(10, 10), sticky="news")

        self.dropdowns = []
        for i, label in enumerate(self.mandatory_columns):
            row = (i // 4) + 1
            col = (i % 4) * 2

            ctk.CTkLabel(mandatory_frame, text=label).grid(row=row, column=col, padx=10, pady=10, sticky="nw")
            dropdown = ctk.CTkOptionMenu(mandatory_frame, width=150, values="", command=self.check_mandatory_fields)
            dropdown.grid(row=row, column=col+1, padx=10, pady=10, sticky="ne")
            dropdown.set("- - - - - - - - -")
            self.dropdowns.append((label, dropdown))

    def create_optional_fields_frame(self, parent):
        optional_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        optional_frame.grid(row=0, column=0, padx=10, pady=(380, 40), sticky="new")
        optional_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(optional_frame, text="Optional Fields Selections", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        self.optional_field_var = StringVar()
        self.optional_field_dropdown = ctk.CTkOptionMenu(optional_frame, variable=self.optional_field_var, values=["No optional field"] + self.optional_columns, width=150)
        self.optional_field_dropdown.grid(row=1, column=0, padx=5, pady=5)
        self.optional_field_dropdown.set("No optional field")

        self.header_var = StringVar()
        self.header_dropdown = ctk.CTkOptionMenu(optional_frame, variable=self.header_var, values=[""], width=150)
        self.header_dropdown.grid(row=1, column=1, padx=5, pady=5)
        self.header_dropdown.set("No Column selected")

        ctk.CTkButton(optional_frame, text="+", width=30, command=self.add_optional_field).grid(row=1, column=2, padx=5, pady=5)

        self.optional_fields_container = ctk.CTkFrame(optional_frame, height=0, fg_color="transparent")
        self.optional_fields_container.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.optional_fields_container.grid_columnconfigure((0, 1, 2), weight=1)

    def create_footer_frame(self):
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(footer_frame, text="Version 1.0", text_color="white", corner_radius=8).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(footer_frame, text="AsteroIdea © 2024", text_color="white", corner_radius=8).grid(row=0, column=0, sticky="e")

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
            messagebox.showerror("Error", "Please enter a file path or choose a file.")
            return

        try:
            result = read_data_with_header(path, header=header_state)
            if result is None:
                messagebox.showerror("Error", "Failed to load the file.")
                return

            if header_state:
                logger.success("Data loaded without headers...")
                headers, data = result if result else ([], None)
            else:
                logger.success("Data loaded with headers...")
                data = result
                headers = data[0].keys() if data else []

            if not data:
                messagebox.showwarning("Warning", "The file appears to be empty.")
                return

            if headers:
                for label, dropdown in self.dropdowns:
                    dropdown.configure(values=[""] + list(headers))
                    dropdown.set("")

                self.header_dropdown.configure(values=[""] + list(headers))
                self.header_dropdown.set("")

            self.check_mandatory_fields()
            logger.success("Data successfully loaded.")

        except Exception as e:
            logger.error(f"An error occurred while processing data: {e}")
            messagebox.showerror("Error", "Please enter a valid file path")

    def update_date_format(self, selected_format):
        global glob_vals
        glob_vals['date_format_val'] = self.date_format_dict.get(selected_format, '%d-%m-%Y')
        logger.info(f"Date Format updated to: {glob_vals['date_format_val']}")

    def open_configuration(self):
        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuration")
        self.config_window.geometry("500x480")
        self.config_window.resizable(True, True)

        self.create_shift_config()
        self.create_zr_config()

        save_button = ctk.CTkButton(self.config_window, text="Save", command=self.save_configuration, width=200)
        save_button.grid(row=10, column=1, columnspan=2, pady=20)

    def create_shift_config(self):
        ctk.CTkLabel(self.config_window, text="SHIFT Infos", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.config_window, text="Computer ID:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.computer_id_entry = ctk.CTkEntry(self.config_window)
        self.computer_id_entry.insert(0, "7077")
        self.computer_id_entry.grid(row=1, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="Device ID:").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.device_id_entry = ctk.CTkEntry(self.config_window)
        self.device_id_entry.insert(0, "799")
        self.device_id_entry.grid(row=2, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="Cashier Contract ID:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.cashier_contract_id_entry = ctk.CTkEntry(self.config_window)
        self.cashier_contract_id_entry.insert(0, "1")
        self.cashier_contract_id_entry.grid(row=3, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="Cashier Consumer ID:").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.cashier_consumer_id_entry = ctk.CTkEntry(self.config_window)
        self.cashier_consumer_id_entry.insert(0, "13")
        self.cashier_consumer_id_entry.grid(row=4, column=2, padx=10, pady=5)

    def create_zr_config(self):
        ctk.CTkLabel(self.config_window, text="ZR Infos", font=("Arial", 14, "bold")).grid(row=5, column=0, padx=10, pady=10, sticky="w")

        ctk.CTkLabel(self.config_window, text="ZR IP:").grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.zr_ip_entry = ctk.CTkEntry(self.config_window)
        self.zr_ip_entry.insert(0, "127.0.0.1")
        self.zr_ip_entry.grid(row=6, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="ZR PORT:").grid(row=7, column=1, padx=10, pady=5, sticky="w")
        self.zr_port_entry = ctk.CTkEntry(self.config_window)
        self.zr_port_entry.insert(0, "8000")
        self.zr_port_entry.grid(row=7, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="ZR Username:").grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.zr_username_entry = ctk.CTkEntry(self.config_window)
        self.zr_username_entry.insert(0, "user")
        self.zr_username_entry.grid(row=8, column=2, padx=10, pady=5)

        ctk.CTkLabel(self.config_window, text="ZR Password:").grid(row=9, column=1, padx=10, pady=5, sticky="w")
        self.zr_password_entry = ctk.CTkEntry(self.config_window)
        self.zr_password_entry.insert(0, "4711")
        self.zr_password_entry.grid(row=9, column=2, padx=10, pady=5)

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

        logger.info(f"Configuration Saved: {configuration_data}")
        self.config_window.destroy()

    def update_load_button_state(self, event=None):
        path = self.path_entry.get().strip()
        self.load_data_button.configure(state="normal" if path else "disabled")

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
        all_selected = all(
            dropdown.get().strip() not in ["No Column selected", "", " ", "- - - - - - - - -"] 
            for _, dropdown in self.dropdowns
        )
        self.button1.configure(state="normal" if all_selected else "disabled")

    


    def create_button_frame(self, parent):
        button_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        button_frame.grid(row=0, column=0, padx=10, pady=(500, 40), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Button 1
        self.button1 = ctk.CTkButton(button_frame, text="Check ZR connection", command=lambda: self.button_action(1))
        self.button1.grid(row=0, column=0, padx=5, pady=20)

        # Button 2
        self.button2 = ctk.CTkButton(button_frame, text="Data validation", command=lambda: self.button_action(2), state="disabled")
        self.button2.grid(row=0, column=1, padx=5, pady=20)

        # Button 3
        self.button3 = ctk.CTkButton(button_frame, text="Start Process", command=lambda: self.button_action(3), state="disabled")
        self.button3.grid(row=0, column=2, padx=5, pady=20)

    def button_action(self, button_number):
        # Reset all button texts
        self.reset_button_texts()

        # Start the loading animation in a separate thread
        Thread(target=self.run_loading_animation, args=(button_number,)).start()

    def create_button_frame(self, parent):
        button_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        button_frame.grid(row=0, column=0, padx=10, pady=(500, 40), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Button 1
        self.button1 = ctk.CTkButton(button_frame, text="Check ZR connection", command=lambda: self.button_action(1))
        self.button1.grid(row=0, column=0, padx=5, pady=20)

        # Button 2
        self.button2 = ctk.CTkButton(button_frame, text="Data validation", command=lambda: self.button_action(2), state="disabled")
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
            print("\n ------------------------------ TEST CONNECTION TO ZR  ------------------------------ \n")
            logger.debug(zr_data)
            zr = test_zr_connection()
            
            # Determine the status of the connection
            if zr == 200:
                logger.info("Test connection established")
                self.code_stat = True 
            elif zr == 404:
                logger.info("Error: Test connection failed")
                self.code_stat = False  
            
            print("----------------------------------------------------------------------------------------- ")

        elif button_number == 2:
            button = self.button2
        else:
            button = self.button3

        # Show loading text/icon
        button.configure(text=f"{button.cget('text').split(' ')[0]} ⏳")

        time.sleep(5)

        # Simulate test result
        test_result = self.simulate_test(button_number)

        # Update the button text based on the test result
        if test_result == 1:
            button.configure(text="Checking Success ✔️")
            logger.info(f"Button {button_number} action succeeded")
            if button_number == 1:
                self.button2.configure(state="normal")  # Enable button 2 if the test succeeds
        else:
            button.configure(text="Error ❌")
            logger.error(f"Button {button_number} action failed")

        # Update button states based on the action taken
        if button_number == 1:
            self.button1.configure(state="disabled")
            # Button 2 is only enabled if the test succeeds (handled above)
            self.button3.configure(state="disabled")
        elif button_number == 2:
            self.button1.configure(state="disabled")
            self.button2.configure(state="disabled")
            self.button3.configure(state="normal")
        else:
            self.button1.configure(state="normal")
            self.button2.configure(state="disabled")
            self.button3.configure(state="disabled")

    def simulate_test(self, button_number):
        # Return the result based on the test for button 1
        if button_number == 1:
            return 1 if self.code_stat else 0
        elif button_number == 2:
            return 1  
        else:
            return 0  # Simulate failure for button 3

    def reset_button_texts(self):
        # Reset all button texts to their original state
        self.button1.configure(text="Check ZR connection")
        self.button2.configure(text="Data validation")
        self.button3.configure(text="Start Process")
        
        

    