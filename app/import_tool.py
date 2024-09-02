import threading
from time import sleep
import tkinter as tk
from tkinter import StringVar, filedialog, messagebox
from tkinter.tix import *
import customtkinter as ctk
from api.api_media import APIClient
from api.shift_api import ShiftPaymentAPIClient
from app.progress_pop import ProcessingPopup
from app.tips_popup import TipsPopup
from classes.error_except import CompanyValidationError, ConsumerValidationError
from classes.validator_class import Company_validation, Consumer_validation
from config.log_config import logger
from functions.dict_xml_user import consumer_to_xml, contract_to_xml
from functions.shift_dict_xml import close_shift_xml, open_shift_xml, topup_pmvc_xml
from functions.test_connect import test_zr_connection
from functions.xml_resp_parser import current_shift_response, get_status_code, open_shift_response, processshift
from globals.global_vars import zr_data, glob_vals, configuration_data, data_validated, validated
from functions.load_data import read_data_with_header

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")    

class PAYG_ImportTool(ctk.CTk):
          
    def __init__(self):
        super().__init__()
        self.title("PAYG Import Tool")


        # Set the geometry of the window
        self.geometry("1300x740")
        self.resizable(False, False)

        # Center the window on the screen
        self.center_cusom()


        """  # Get the user's screen size
        screen_width = self.config_window.winfo_screenwidth()
        screen_height = self.config_window.winfo_screenheight()

        # Set the window size to 80% of the screen size, for example
        window_width = int(screen_width * 0.25)
        window_height = int(screen_height * 0.58)

        # Set the window size and position
        self.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")"""

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
            "Company_id", "Company_Name", "Company_ValidFrom", "Company_ValidUntil", "Participant_Id",
            "Participant_Firstname", "Participant_Surname","Participant_CardNumber",
            "Participant_ValidFrom","Participant_ValidUntil", 
        ]
        self.optional_columns = [
            "Company_Surname", "Company_phone1", "Company_email1",
            "Company_Street", "Company_Town","Company_Postbox","Company_FilialId", 
            "Participant_FilialId", "Participant_Type","Participant_Cardclass", 
            "Participant_IdentificationType","Participant_Present", "Participant_Status", 
            "Participant_GrpNo","Participant_DisplayText","Participant_LPN1", 
            "Participant_LPN2", "Participant_LPN3", "Amount"
        ]
        
        #tool_tip = Balloon(self)

       
        self.optional_field_count = 0
        self.optional_fields = []
        self.file_stat = False
        self.state_popup = True

        logger.info("Starting UI in progress . . .")


        self.setup_ui()
        self.after(100, self.show_tips_popup)
        
        self.shift_api = ShiftPaymentAPIClient()    
        self.api_client = APIClient()
            
    def show_tips_popup(self):
        if self.state_popup:
            tips_popup = TipsPopup(self)
            tips_popup.grab_set()  
            
    def open_tip(self):
        tips = TipsPopup(self)
        tips.open_popup_tips()
        tips.grab_set()  
        logger.info("TIPS Window opened ")
            
            
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.create_title_frame()
        self.create_main_frame()
        self.create_footer_frame()

    def center_cusom(self):
        # Calculate the position for the window to be centered
        window_width = 1300
        window_height = 740
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        # Set the window's position
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
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

    def get_text_color():
        appearance_mode = ctk.get_appearance_mode()
        if appearance_mode == "Dark":
            return "white"
        if appearance_mode == "Light":
            return "black"
    text_color = get_text_color()


# ------------------------------------- Titile Frame ----------------------------------------------------
    def create_title_frame(self):
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            title_frame,
            text="PAYG Import Tool",
            font=("Arial", 24, "bold"),
            text_color=self.text_color,
            corner_radius=8
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            title_frame,
            text=" ✔️Configuration ",
            text_color="black",
            border_color=self.text_color,
            width=30,
            height=30,
            fg_color="white",
            hover_color=("gray70", "gray30"),
            command=self.open_configuration
        ).grid(row=0, column=2, sticky="e", padx=(0, 10))
        
        ctk.CTkButton(
            title_frame,
            text="ⓘ How to use",
            text_color="black",
            border_color=self.text_color,
            width=30,
            height=30,
            fg_color="white",
            hover_color=("gray70", "gray30"),
            command=self.open_tip
        ).grid(row=0, column=3, sticky="e", padx=(0, 10))
# ------------------------------------- Titile Frame - Compns ----------------------------------------------------
    
    def open_configuration(self):
        if hasattr(self, 'config_window') and self.config_window.winfo_exists():
            self.config_window.lift()
            return

                
        logger.info(f"Configuration Popup opened")

        self.create_blurred_overlay()

        # Create the configuration window
        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuration")

        # Get the user's screen size
        #screen_width = self.config_window.winfo_screenwidth()
        #screen_height = self.config_window.winfo_screenheight()

        # Set the window size to 80% of the screen size, for example
        #window_width = int(screen_width * 0.25)
        #window_height = int(screen_height * 0.58)

        # Set the window size and position
        #self.config_window.geometry(f"{window_width}x{window_height}+{int((screen_width - window_width) / 2)}+{int((screen_height - window_height) / 2)}")
        self.config_window.resizable(False, False)

        #self.config_window.geometry(" W x H")
        self.config_window.geometry("480x630")

        # Center the config window (might be redundant now)

        self.create_zr_config()
        self.create_shift_config()

        # Load saved data
        self.load_configuration_data()

        ctk.CTkLabel(self.config_window, text="", font=("Arial", 14, "bold")).grid(row=13, column=0, pady=15, sticky="w")

        self.save_button = ctk.CTkButton(self.config_window, text="Save", fg_color='green', command=self.save_configuration, width=150, state="normal")
        self.save_button.grid(row=15, column=1, padx=5, pady=10)
    
        self.cancel = ctk.CTkButton(self.config_window, text="Cancel", fg_color='red', command=self.on_config_close, width=150, state="normal")
        self.cancel.grid(row=15, column=2, padx=5, pady=10)
        
        # Make the configuration window modal
        self.config_window.transient(self)
        self.config_window.grab_set()
        self.config_window.protocol("WM_DELETE_WINDOW", self.on_config_close)
        self.wait_window(self.config_window)

    def check_connection(self, connection_type):
        button = self.check_zr_button if connection_type == 'zr' else self.check_shift_button
        
        # Start the loading animation in a separate thread
        threading.Thread(target=self.run_check_animation, args=(connection_type, button)).start()

    def run_check_animation(self, connection_type, button):
        original_text = button.cget('text')
        button.configure(text=f"{original_text} ⏳", state="normal")

        # Simulate check
        if connection_type == 'zr':
            success = self.check_zr()
            
        if connection_type == 'shift':
            success = self.check_shift()

        if success:
            button.configure(text=f"{original_text} ✔️", fg_color="green")
            logger.info(f"{connection_type.upper()} check succeeded")
        else:
            button.configure(text=f"{original_text} ❌", fg_color="red")
            logger.error(f"{connection_type.upper()} check failed")
            self.config_window.after(2000, lambda: button.configure(text="Retry", fg_color='dodgerblue3', state="normal"))

        # Check if both ZR and Shift checks were successful
        self.update_save_button_state()
          
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
        ctk.CTkLabel(self.config_window, text="ZR Infos", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Check ZR button
        self.check_zr_button = ctk.CTkButton(self.config_window, text="Check ZR", command=lambda: self.check_connection('zr'), width=200)
        self.check_zr_button.grid(row=6, column=1,columnspan=2, padx=(30,0), pady=10, sticky="w")

        ctk.CTkLabel(self.config_window, text="ZR IP:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.zr_ip_entry = ctk.CTkEntry(self.config_window)
        self.zr_ip_entry.insert(0, "127.0.0.1")
        self.zr_ip_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.config_window, text="ZR PORT:").grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.zr_port_entry = ctk.CTkEntry(self.config_window)
        self.zr_port_entry.insert(0, "8443")
        self.zr_port_entry.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.config_window, text="ZR Username:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.zr_username_entry = ctk.CTkEntry(self.config_window)
        self.zr_username_entry.insert(0, "6")
        self.zr_username_entry.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.config_window, text="ZR Password:").grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.zr_password_entry = ctk.CTkEntry(self.config_window, show="*")
        self.zr_password_entry.insert(0, "4711")
        self.zr_password_entry.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(self.config_window, text="Timout Calls (ms):").grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.timout_entry = ctk.CTkEntry(self.config_window)
        self.timout_entry.insert(0, "1000")
        self.timout_entry.grid(row=5, column=2, padx=10, pady=5, sticky="w")
        
        #ctk.CTkLabel(self.config_window, text="", font=("Arial", 14, "bold")).grid(row=7, column=0, pady=(10, 5), sticky="w")

    def create_shift_config(self):
        ctk.CTkLabel(self.config_window, text="SHIFT Infos", font=("Arial", 14, "bold")).grid(row=7, column=0, padx=10, pady=10, sticky="w")

        # Check Shift button
        self.check_shift_button = ctk.CTkButton(self.config_window, text="Check Shift", command=lambda: self.check_connection('shift'), width=200)
        self.check_shift_button.grid(row=13, column=1,columnspan=2, padx=(30,0), pady=10, sticky="w")

        ctk.CTkLabel(self.config_window, text="Computer ID:").grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.computer_id_entry = ctk.CTkEntry(self.config_window)
        self.computer_id_entry.insert(0, "7077")
        self.computer_id_entry.grid(row=8, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.config_window, text="Device ID:").grid(row=9, column=1, padx=10, pady=5, sticky="w")
        self.device_id_entry = ctk.CTkEntry(self.config_window)
        self.device_id_entry.insert(0, "799")
        self.device_id_entry.grid(row=9, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.config_window, text="Cashier Contract ID:").grid(row=10, column=1, padx=10, pady=5, sticky="w")
        self.cashier_contract_id_entry = ctk.CTkEntry(self.config_window)
        self.cashier_contract_id_entry.insert(0, "1")
        self.cashier_contract_id_entry.grid(row=10, column=2, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self.config_window, text="Cashier Consumer ID:").grid(row=11, column=1, padx=10, pady=5, sticky="w")
        self.cashier_consumer_id_entry = ctk.CTkEntry(self.config_window)
        self.cashier_consumer_id_entry.insert(0, "13")
        self.cashier_consumer_id_entry.grid(row=11, column=2, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(self.config_window, text="Shift ID:").grid(row=12, column=1, padx=10, pady=5, sticky="w")
        self.shift_id_entry = ctk.CTkEntry(self.config_window, state='disabled')
        self.shift_id_entry.insert(0, "0")
        self.shift_id_entry.grid(row=12, column=2, padx=10, pady=5, sticky="w")
    
    def save_configuration(self):
        global configuration_data

        configuration_data['zr_ip'] = self.zr_ip_entry.get().strip()
        configuration_data['zr_port'] = self.zr_port_entry.get().strip()
        configuration_data['username'] = self.zr_username_entry.get().strip()
        configuration_data['password'] = self.zr_password_entry.get().strip()
        configuration_data['computer_id'] = self.computer_id_entry.get().strip()
        configuration_data['device_id'] = self.device_id_entry.get().strip()
        configuration_data['cashier_contract_id'] = self.cashier_contract_id_entry.get().strip()
        configuration_data['cashier_consumer_id'] = self.cashier_consumer_id_entry.get().strip()
        configuration_data['shift_id'] = self.shift_id_entry.get().strip()
        configuration_data['timeout'] = self.timout_entry.get().strip()

        # Save shift ID if it exists

        logger.info(f"Configuration Saved: {configuration_data}")
        self.overlay.destroy()
        self.config_window.destroy()
        
    def save_config(self):
        global configuration_data

        configuration_data['computer_id'] = self.computer_id_entry.get().strip()
        configuration_data['device_id'] = self.device_id_entry.get().strip()
        configuration_data['cashier_contract_id'] = self.cashier_contract_id_entry.get().strip()
        configuration_data['cashier_consumer_id'] = self.cashier_consumer_id_entry.get().strip()
        configuration_data['shift_id'] = self.shift_id_entry.get().strip()
        configuration_data['timeout'] = self.timout_entry.get().strip()

        configuration_data['zr_ip'] = self.zr_ip_entry.get().strip()
        configuration_data['zr_port'] = self.zr_port_entry.get().strip()
        configuration_data['username'] = self.zr_username_entry.get().strip()
        configuration_data['password'] = self.zr_password_entry.get().strip()

        # Save shift ID if it exists
        self.shift_api = ShiftPaymentAPIClient() 
        self.api_client = APIClient()
        
        # Remove the 'password' key from the original configuration_data for logging
        config_data_without_password = {key: value for key, value in configuration_data.items() if key != 'password'}

        # Log the configuration data without the password
        logger.info(f"Configuration Saved: {config_data_without_password} \n")

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
        
        self.shift_id_entry.delete(0, 'end')
        self.shift_id_entry.insert(0, configuration_data['shift_id'])
        
        self.zr_ip_entry.delete(0, 'end')
        self.zr_ip_entry.insert(0, configuration_data['zr_ip'])
        
        self.zr_port_entry.delete(0, 'end')
        self.zr_port_entry.insert(0, configuration_data['zr_port'])
        
        self.zr_username_entry.delete(0, 'end')
        self.zr_username_entry.insert(0, configuration_data['username'])
        
        self.zr_password_entry.delete(0, 'end')
        self.zr_password_entry.insert(0, configuration_data['password'])
        
        self.timout_entry.delete(0, 'end')
        self.timout_entry.insert(0, configuration_data['timeout'])
        
        load_data = {configuration_data['computer_id'],configuration_data['device_id'],configuration_data['cashier_contract_id'],
                    configuration_data['cashier_consumer_id'],configuration_data['shift_id'],configuration_data['zr_ip'],
                    configuration_data['username'] ,  configuration_data['timeout']}
        
        logger.info('Existing Configuration Data Loaded - - - - ')
        logger.info(f'Existing Configuration Data Loaded - - - - {load_data}')
        logger.debug(f'Existing Configuration Data Loaded - - - -  {load_data}')

    def check_zr(self):
        self.save_config()
        
        print("\n ------------------------------ TEST CONNECTION TO ZR  ------------------------------ \n")
        logger.debug(zr_data)
        zr = test_zr_connection()
        
        if zr == 200:
            logger.info("Connection Success to ZR  ✔️")
            self.code_stat = True 
            self.check_zr_button.configure
            
            return True
        else:
            logger.info("Connection Failed to ZR  ❌")
            self.code_stat = False  
            return False
        
    def check_shift(self):
        
        self.save_config()
        #print(self.zr_ip_entry.get().strip())
        print("\n ------------------------------ TEST CONNECTION TO SHIFT ------------------------------ \n")
        try:
            shift_id = self.ensure_open_shift()
            if shift_id:
                # Shift is open, add field with shift ID
                self.shift_id_entry.configure(state='normal')  # Enable entry field to update it
                self.shift_id_entry.delete(0, 'end')  # Clear the current content
                self.shift_id_entry.insert(0, shift_id)  # Insert the new shift ID
                self.shift_id_entry.configure(state='disabled')  # Re-disable entry field
                return True
            else:
                # No shift open, show popup
                response = messagebox.askyesno("No Open Shift", "No shift is currently open. Would you like to open a shift?")
                if response:
                    # User wants to open a shift
                    op_shift = open_shift_xml()
                    status_code, shift_detail = self.shift_api.open_shift_api(op_shift)
                    logger.debug(f"Shift Reponse Detail : {shift_detail}")
                    
                    #input()
                    
                    
                    if shift_detail is not None:
                        try:
                            _, new_shift_id, _ = current_shift_response(shift_detail)
                            #print(shift_detail)
                            if new_shift_id:
                                logger.info(f"New shift {new_shift_id} opened.")
                                #self.shift_id_entry.insert(0, new_shift_id)  
                                 # Shift is open, add field with shift ID
                                self.shift_id_entry.configure(state='normal') 
                                self.shift_id_entry.delete(0, 'end')  
                                self.shift_id_entry.insert(0, new_shift_id)  
                                self.shift_id_entry.configure(state='disabled')  
                                
                                return True
                            else:
                                logger.error("Failed to get new shift ID")
                                messagebox.showerror("Error", "Failed to open a new shift.")
                                return False
                        except Exception as e:
                            logger.error(f"Error parsing shift response: {str(e)}" )
                            #messagebox.showerror("Error", "Failed to parse shift response.")
                            return False
                    else:
                        logger.error("Shift API returned None for shift_detail")
                        messagebox.showerror("Error", "Failed to get shift details from API.")
                        return False
                else:
                    logger.info("User chose not to open a new shift")
                    return False
        except Exception as e:
            logger.error(f"Error checking shift: {str(e)}" )
            messagebox.showerror("Error", f"An error occurred while checking the shift: {str(e)}")
            return False
    
    def update_save_button_state(self):
        zr_success = self.check_zr_button.cget('fg_color') == 'green'
        shift_success = self.check_shift_button.cget('fg_color') == 'green'

        if zr_success or shift_success:
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="normal")

# -----------------------------------------------------------------------------------------------------



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
        file_data_frame.grid(row=0, column=0, padx=10, pady=(5, 20), sticky="new")
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
        pmvc_check = ctk.CTkCheckBox(file_data_frame, text="PMVC Topup", variable=self.pmvc_var).grid(row=1, column=9, padx=5, pady=(5, 5))
        self.pmvc_var.trace_add('write', self.update_columns)
        
        #tool_tip = Balloon(file_data_frame)
        #tool_tip.bind(pmvc_check, "Check this box if you want to include PMVC Topup")
        
        # Template ID section
        #ctk.CTkLabel(file_data_frame, text="Template ID:", font=("Arial", 14, "bold")).grid(row=2, column=0, padx=(10, 5), pady=(5, 5), sticky="w")

        # Season Parker ID
        ctk.CTkLabel(file_data_frame, text="Season Parker template ID:").grid(row=2, column=0, padx=5,  pady=5, sticky="e")
        self.template1_var = StringVar(value="3")
        self.template1_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template1_var, width=50)
        self.template1_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # PMVC ID
        ctk.CTkLabel(file_data_frame, text="PMVC template ID:").grid(row=2, column=2, padx=5, pady=5, sticky="e")
        self.template2_var = StringVar(value="100")
        self.template2_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template2_var, width=50)
        self.template2_entry.grid(row=2, column=3, padx=5, pady=5, sticky="ew")

        # CPM ID
        ctk.CTkLabel(file_data_frame, text="Company template ID:").grid(row=2, column=4, padx=5, pady=5, sticky="e")
        self.template3_var = StringVar(value="2")
        self.template3_entry = ctk.CTkEntry(file_data_frame, textvariable=self.template3_var, width=50)
        self.template3_entry.grid(row=2, column=5, padx=5, pady=5, sticky="ew")
        

        ctk.CTkLabel(file_data_frame, text="Date Format:").grid(row=2, column=7, padx=5, pady=(5, 5), sticky="e")
        self.date_format_var = StringVar(value="yyyy-mm-dd")
        ctk.CTkOptionMenu(file_data_frame, variable=self.date_format_var, values=list(self.date_format_dict.keys()), width=150, command=self.update_date_format).grid(row=2, column=8, columnspan=2, padx=5, pady=5, sticky="w")

        self.load_data_button = ctk.CTkButton(file_data_frame, text="Load Data ", hover = None, command=self.load_file_data, state="disabled")
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
                self.load_data_button.configure(text="Load Data", state="normal", fg_color='dodgerblue3')  # Reset to default
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
                data = result
                headers = result[0].keys() if result else ()
                                
                print(" / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /")
                print(headers)  
                print(" / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /")
                print(data)
                print(" / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /")
                
            else:
                logger.success("Data loaded with headers...")

                data = result
                headers = data[0].keys() if data else []
                
                print("****************************************************************")
                print(headers)
                print("****************************************************************")
                print(data)
                print("****************************************************************")
                
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

    
# ------------------------------------- Main Frame - Compns - madatory fild  -------------------------------

    def create_mandatory_fields_frame(self, parent):
        self.mandatory_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        self.mandatory_frame.grid(row=0, column=0, padx=10, pady=(190, 40), sticky="new")
        self.mandatory_frame.grid_columnconfigure((1, 3, 5, 7, 9), weight=1)

        ctk.CTkLabel(self.mandatory_frame, text="Mandatory Fields Selections", font=("Arial", 18, "bold")).grid(row=0, column=0, columnspan=10, padx=10, pady=(10, 10), sticky="news")
        
        self.update_mandatory_fields()

    def update_mandatory_fields(self):
        # Clear existing widgets
        for widget in self.mandatory_frame.winfo_children():
            if isinstance(widget, (ctk.CTkOptionMenu, ctk.CTkLabel)) and widget.winfo_y() > 50:  # Preserve the title
                widget.destroy()

        self.dropdowns = []

        for i, label in enumerate(self.mandatory_columns):
            row = (i // 4) + 1
            col = (i % 4) * 2

            ctk.CTkLabel(self.mandatory_frame, text=label).grid(row=row, column=col, padx=10, pady=10, sticky="news")
            dropdown = ctk.CTkOptionMenu(self.mandatory_frame, width=150, values="", command=self.check_mandatory_fields)
            dropdown.grid(row=row, column=col+1, padx=10, pady=10, sticky="news")
            dropdown.set("- - - - - - - - -")
            self.dropdowns.append((label, dropdown))   
    
    def on_data_loaded(self, status):
    # Update the status label to show success when data is loaded
        if status == "success":
            self.file_stat = True
            self.load_data_button.configure(text="✔ Data Loaded", fg_color="green")
            self.validation.configure(text=f"Validate Data", state="normal", fg_color='dodgerblue3')

        if status == "error":
            self.file_stat = True
            self.load_data_button.configure(text="✘ Error", fg_color="red")
            self.validation.configure(text=f"Error Reading file ❌", fg_color="red", state="normal")

    def check_mandatory_fields(self, *args):
        all_selected = all(
            dropdown.get().strip() not in ["", "No Column selected", "- - - - - - - - -"]
            for _, dropdown in self.dropdowns
        )
        
        # The status icon in this function is unrelated to data load status
        self.process.configure(state="normal" if all_selected else "disabled")
        self.validation.configure(state="normal" if all_selected else "disabled")

    def update_columns(self, *args):
        pmvc_fields = ["Amount", "Participant_Type"]

        if self.pmvc_var.get():
            # Move fields to mandatory, ensuring they are not duplicated
            self.mandatory_columns.extend([field for field in pmvc_fields if field not in self.mandatory_columns])
            self.optional_columns = [field for field in self.optional_columns if field not in pmvc_fields]
        else:
            # Move fields to optional, ensuring they are not duplicated
            self.optional_columns.extend([field for field in pmvc_fields if field not in self.optional_columns])
            self.mandatory_columns = [field for field in self.mandatory_columns if field not in pmvc_fields]

        self.update_mandatory_fields()
        self.update_optional_fields_dropdown()  
        self.load_file_data()

# ------------------------------------------------------------------------------------------------------------



# ------------------------------------- Main Frame - Compns - optional fild  -----------------------------------
    def create_optional_fields_frame(self, parent):
        self.optional_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        self.optional_frame.grid(row=0, column=0, padx=10, pady=(390, 40), sticky="new")
        self.optional_frame.grid_columnconfigure((1, 2, 3, 4), weight=1)

        ctk.CTkLabel(self.optional_frame, text="Optional Fields Selections", font=("Arial", 18, "bold")).grid(row=0, columnspan=10, padx=10,  pady=(10,10), sticky="news")

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
        self.optional_fields_container.configure(height=60)  

        self.optional_fields = []

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
        self.update_frame_size()    
        
    def update_optional_fields_dropdown(self):
        current_options = [field for field in self.optional_columns if field not in [f[0] for f in self.optional_fields]]
        if not current_options:
            current_options = ["No optional field"]
        self.optional_field_dropdown.configure(values=current_options)
        self.optional_field_dropdown.set(current_options[0])
        
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

        self.update_frame_size()

    def update_frame_size(self):
        if self.optional_fields:
            total_height = sum(frame.winfo_reqheight() for _, _, _, frame in self.optional_fields)
            self.optional_fields_container.configure(height=max(30, total_height))  
        else:
            self.optional_fields_container.configure(height=30) 
        self.optional_frame.update_idletasks()
# ---------------------------------------------------------------------------------------------------------------
 
    
    
# ------------------------------------- Main Frame - Compns - Button process fild  ------------------------------
    def create_button_frame(self, parent):
        button_frame = ctk.CTkFrame(parent, corner_radius=10, border_width=2)
        button_frame.grid(row=0, column=0, padx=10, pady=(550, 40), sticky="new")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)
        

        # Button 1: Validate DAta 
        self.validation = ctk.CTkButton(button_frame, width=160, height=35, text="Validate Data", state="normal", command=self.validating_data)
        self.validation.grid(row=0, column=0, padx=5, pady=10)
        
        # Timeline Label
        self.timeline_label = ctk.CTkLabel(button_frame, text="-------------------------------------------------------")
        self.timeline_label.grid(row=0, column=1, padx=5, pady=20)
        
        # Button 2: Start Process
        self.process = ctk.CTkButton(button_frame, width=160, height=35, text="Start Process", command=self.main_process, state="disabled")
        self.process.grid(row=0, column=2, padx=5, pady=10)
        
    def validating_data(self):
        global data_validated, configuration_data   
        shifts = configuration_data

        self.validation.configure(text="Validating data ⏳", state="normal")

        popup = ProcessingPopup(self)
        popup.update_status("Initializing data validation process... ")        
        popup.update_progress(0)  # Start at 0%

        self.api_client = APIClient()


        logger.info("Starting data validation process")
        sleep(1)
        
        header_state = self.no_headers_var.get()
        popup.update_status(f"Header State: {'No Headers' if header_state else 'Headers Present'}  ")
        logger.debug(f"Header State: {header_state}")

        file_path = self.path_entry.get()
        popup.update_status("Reading CSV file...  ")
        logger.info(f"Attempting to read CSV file: {file_path}")
        popup.update_progress(10)  # Start at 0%

        sleep(1)

        try:
            file_data = read_data_with_header(file_path, header_state)
            logger.debug(f"CSV data read successfully. First few rows: {file_data[:5]}")
            popup.show_success("CSV file read successfully  ")
            popup.update_progress(15)  # Start at 0%
        except Exception as e:
            self.validation.configure(text="Error Reading File ❌", fg_color="red")
            logger.error(f"Failed to read CSV file: {str(e)}")
            
            self.config_window.after(2000, lambda: self.validation.configure(text="Retry Process", fg_color='dodgerblue3', state="normal"))
            
            popup.show_error(f"Failed to read CSV file: {str(e)}  ")
            popup.enable_ok_button()
            return

        popup.update_status("Processing selected fields...   \n")
        logger.info("Mapping selected fields to data columns")
        mymappingdict = {}
        popup.update_progress(20)
        sleep(1)
        
        for label, dropdown in self.dropdowns:
            if dropdown.get():
                mymappingdict[label] = dropdown.get()
            else:
                mymappingdict[label] = "NOSELECTED"

        for name, header in self.optional_fields:
            logger.debug(f"Optional field mapping: {name} -> {header}")
            mymappingdict[name] = header

        popup.update_status("Extracting data from selected fields...   \n")
        logger.info("Extracting data based on field mapping")
        
        data_rows = []
        for row in file_data:
            newdict = {k: row.get(v, 'ERROR') for k, v in mymappingdict.items()}
            data_rows.append(newdict)
            logger.debug(f"Processed row: {newdict}")
        
        logger.debug(f"Total rows processed: {len(data_rows)}")
        logger.debug(f"Field mapping: {mymappingdict}")

        popup.update_status("Validating data...  ")
        logger.info("Starting data validation for companies and participants")

        sleep(1)

        company_ids = set()
        for row in data_rows:
            # Company validation
            try:
                company_valid = Company_validation(**row)
                cid = row.get('Company_id')
                if cid not in company_ids:
                    data_validated['mylistc'].append(company_valid.dict())
                    company_ids.add(cid)
                    logger.info(f"Validated company: {row.get('Company_Name', 'Unknown')} (ID: {cid})")
                    popup.show_success(f"Validated company in file : {row.get('Company_Name', 'Unknown')} (ID: {cid})  ")
            except CompanyValidationError as e:
                error_message = str(e)
                self.validation.configure(text="Error Validation ❌", fg_color="red")
                logger.error(f"Company validation failed: {error_message}")
                self.config_window.after(2000, lambda: self.validation.configure(text="Retry Validation", fg_color='dodgerblue3', state="normal"))
                self.process.configure(state="normal")

                popup.destroy()
                response = self.custom_retry_continue_dialog(
                    "Company Data Validation",
                    f"Validation failed: {error_message}\nDo you want to retry or exit?"
                )
                if response == "exit":
                    popup.destroy()
                    return
            except Exception as e:
                logger.error(f'Unexpected error during company validation: {str(e)}')

            # Participant validation
            try:
                participant_valid = Consumer_validation(**row)
                data_validated['mylistp'].append(participant_valid.dict())
                logger.info(f"Validated participant: {row.get('Participant_Id', 'Unknown')}")
                popup.show_success(f"Validated participant in file : {row.get('Participant_Id', 'Unknown')}")
            except ConsumerValidationError as e:
                error_message = str(e)
                self.validation.configure(text="Error Validation ❌", fg_color="red")
                self.process.configure(state="normal")
                logger.error(f"Consumer validation failed: {error_message}")
                self.config_window.after(2000, lambda: self.validation.configure(text="Retry Validation", fg_color='dodgerblue3', state="normal"))

                popup.destroy()
                response = self.custom_retry_continue_dialog(
                    "Consumer Data Validation",
                    f"Validation failed: {error_message}\nDo you want to retry or exit?"
                )
                if response == "exit":
                    popup.destroy()
                    return
        popup.update_progress(30)
        sleep(1)
        self.validation.configure(text="Validation Success ✔️", fg_color="green")
        self.process.configure(state="normal")
        self.validation.configure(state="normal")

        logger.info("Data validation completed successfully")
        popup.show_success("Data Validation Success ")
        
        logger.debug(f"Validated companies: {len(data_validated['mylistc'])}")
        logger.debug(f"Validated participants: {len(data_validated['mylistp'])}")
        
        sleep(1)
        self.validation.configure(text="Checking data with ZR ⏳", state="normal",fg_color='dodgerblue3')


        popup.update_status(" Checking Company's in System Started . . .   ")
        logger.debug(f"checking company's in progress")

        mylistc_data = data_validated['mylistc']
        mylistp_data = data_validated['mylistp']

        timeout = (int(shifts["timeout"])*0.001)
        print(timeout)
        
        #print(mylistc_data)
        #input()
        
        logger.debug(f"------------------------------------------Validation Started with ZR  ---------------------------------------------")

        #-------------------------------------------------------- COMPANY --------------------------------------------------------
        popup.update_progress(40)
        logger.debug(mylistc_data)
        print('\n')
        logger.debug(mylistp_data)
        
        for rowc in mylistc_data:
            company_id = rowc.get('Company_id')
            company_name = rowc.get('Company_Name')
            popup.update_status(f"Processing company: {company_name}  ")
                
            status_code, company_details = self.api_client.get_company_details(company_id)
            logger.debug(f"Company details {company_name} - {company_id}: {company_details}")
            
            sleep(timeout)
            
            if status_code != 404:
                popup.show_success(f"Company ID {company_id} found  ")
                
            else:
                popup.show_error(f"Company ID {company_id} not found. Creating new company...  ")
                try:
                    xml_comp_data = contract_to_xml(rowc)
                    status_code, result = self.api_client.create_company(xml_comp_data)
                    
                    if status_code == 201:
                        popup.show_success(f"Company ID {company_id} created successfully  ")
                    else:
                        popup.show_error(f"Failed to create Company ID {company_id}. Status code: {status_code}  ")
                except Exception as e:
                    popup.show_error(f"Error creating Company {company_id} -- ERROR : {e}  ")
            
        popup.update_progress(80)
        
        popup.show_success(" Checking Company's in System Ended")
        logger.debug(f"Checking Company's in System Ended")
        #-------------------------------------------------------- END COMPANY --------------------------------------------------------
        print("\n")
        
        #-------------------------------------------------------- PARTICIPANT --------------------------------------------------------
                
        popup.update_progress(60)
               

        #-------------------------------------------------------- END COMPANY --------------------------------------------------------
        popup.update_progress(82)

        sleep(1)
        self.validation.configure(text="Checking in ZR complete ✔️", fg_color="green")
        logger.debug(f"------------------------------------------Validation Completed ---------------------------------------------")
        popup.update_progress(100)

        return data_validated['mylistc'], data_validated['mylistp']
 
    def main_process(self):
        global glob_vals, configuration_data, data_validated
        template_ids = glob_vals
        shifts = configuration_data
        
        #mylistc_data = data_validated['mylistc']
        mylistp_data = data_validated['mylistp']

        self.process.configure(text=f"Processing ⏳", state="normal")

        timeout = (int(shifts["timeout"])*0.001)
        
        self.shift_api = ShiftPaymentAPIClient()
        self.api_client = APIClient()

        popup = ProcessingPopup(self)
        popup.update_status(f"Starting API Calls with timeout {timeout}...   ")
        logger.debug(f"Starting API Calls with timeout {timeout}")



        popup.update_status("Processing participants in progress ...  ")
        
        amount_mandatory = "Amount" in self.mandatory_columns
        participant_type_mandatory = "Participant_Type" in self.mandatory_columns

        for rowp in mylistp_data:
            participant_id = rowp.get('Participant_Id')
            company_id = rowp.get('Company_id')
            participant_type = rowp.get('Participant_Type') if participant_type_mandatory else None
            amount = rowp.get('Amount') if amount_mandatory else None

            popup.update_status(f"Processing participant: {participant_id} -- Company {company_id} ")

            if not participant_type_mandatory:
            
                if status_code != 404 or status_code != 500:
                    popup.update_status(f"Creating new participant ID {participant_id} for Company ID {company_id}  ")
                    logger.info(f"Creating new participant ID {participant_id} for Company ID {company_id}  \n")            
                    template_id = template_ids["season_parker"]
                    sleep(timeout)

                    xml_ptcpt_data = consumer_to_xml(rowp)
                    status_code, result = self.api_client.create_participant(company_id, template_id, xml_ptcpt_data.strip())

                    if status_code == 201:
                        popup.show_success(f"Participant ID {participant_id} created successfully for Company ID {company_id}  ")
                        logger.success(f"Participant ID {participant_id} created successfully for Company ID {company_id} ")
                    else:
                        popup.show_error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}")
                        logger.error(f"Failed to create Participant ID {participant_id}")

            if participant_type_mandatory:

                if participant_type == 2:
                    status_code, participant_details = self.api_client.get_participant(company_id, participant_id)

                    if status_code != 404:
                        popup.show_success(f"Participant ID {participant_id} found for Company ID {company_id}")
                        logger.success(f"Participant ID {participant_id} found for Company ID {company_id}")
                    else:
                        popup.update_status(f"Creating new participant ID {participant_id} for Company ID {company_id}")
                        logger.info(f"Creating new participant ID {participant_id} for Company ID {company_id}")
                        template_id = template_ids["season_parker"]

                        sleep(timeout)

                        xml_ptcpt_data = consumer_to_xml(rowp)
                        status_code, result = self.api_client.create_participant(company_id, template_id, xml_ptcpt_data)

                        if status_code == 201:
                            popup.show_success(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                            logger.success(f"Creating new participant ID {participant_id} for Company ID {company_id}")

                        else:
                            popup.show_error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

                elif participant_type == 6:
                    
                    
                    shift_id = shifts["shift_id"]

                    if amount_mandatory:
                        
                        status_code, participant_details = self.api_client.get_participant(company_id, participant_id)

                        if status_code != 404:
                            popup.show_success(f"Participant ID {participant_id} found for Company ID {company_id}")
                        else:
                            popup.update_status(f"Creating new participant ID {participant_id} for Company ID {company_id}")
                            template_id = template_ids["pmvc"]
                            xml_ptcpt_data = consumer_to_xml(rowp)
                            
                            sleep(5)

                            status_code, result = self.api_client.create_participant(company_id, template_id, xml_ptcpt_data)

                            if status_code != 201:
                                popup.show_error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")
                                continue
                        
                        money_balance = amount
                        logger.debug(money_balance)
                        
                        if int(money_balance) > 0:
                            popup.update_status(f"Performing TOPUP for Participant ID {participant_id}")
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

                            sleep(timeout)
                            logger.debug(data)
                            
                            data_topup_xml = topup_pmvc_xml(shift_id, data)
                            logger.debug(data_topup_xml)
                            
                            status_code_tp, shift_detail = self.shift_api.topup_pmvc_api(shift_id, data_topup_xml)

                            if status_code_tp == 200 or status_code_tp == 201:
                                popup.show_success("TOPUP completed successfully")
                                logger.success(f"TOPUP completed successfully for participant {participant_id} -- Company {company_id}") 
                                
                                
                            else:
                                popup.show_error(f"Error Occured . . .")
                                logger.error(f"TOPUP failed. Status code: {status_code_tp}") 
                                continue

                        elif int(money_balance) == 0:
                            popup.show_success("Topup amount is 0 for participant ")
                            continue
                    else:
                        popup.update_status("Processing PMVC participant without topup.")


                        status_code, participant_details = self.api_client.get_participant(company_id, participant_id)

                        if status_code != 404:
                            popup.show_success(f"Participant ID {participant_id} found for Company ID {company_id}")
                        else:
                            popup.update_status(f"Creating new participant ID {participant_id} for Company ID {company_id}")
                            template_id = template_ids["pmvc"]
                            
                            sleep(timeout)

                            xml_ptcpt_data = consumer_to_xml(rowp)
                            status_code, result = self.api_client.create_participant(company_id, template_id, xml_ptcpt_data)

                            if status_code == 201:
                                popup.show_success(f"Participant ID {participant_id} created successfully for Company ID {company_id}")
                            else:
                                popup.show_error(f"Failed to create Participant ID {participant_id} for Company ID {company_id}. Status code: {status_code}")

        popup.update_status("Processed Successfully !")
        self.process.configure(text=f"Processed Successfully ✔", fg_color="green")

        popup.enable_ok_button()       
# -----------------------------------------------------------------------------------------------------------------



# ------------------------------------- Main Frame - Compns - Shift Part  ------------------------------
    def ensure_open_shift(self):
        try:
            # Fetch current shift details
            curr_status_code, curr_shift_detail = self.shift_api.get_current_shift_api(1)
            logger.debug(f"Current shift details: {curr_shift_detail}")
            
            if curr_shift_detail is None:
                logger.error("API returned None for current shift details")
                return None

            # Determine the status code from the shift details
            stat = get_status_code(curr_shift_detail)

            if stat in [200, 201]:
                # Extract shift information if the status is 200 or 201
                shift_status, shift_id, shift_no = current_shift_response(curr_shift_detail)
                logger.info(f"SHIFT Status: {shift_status} -- SHIFT ID: {shift_id} -- SHIFT NO: {shift_no}")
                logger.info(f"SHIFT ID: {shift_id} is already opened")
                
                return shift_id
            
            if stat == 500:
                # Handle the case where no open shift is found
                logger.info("No open shift found. A new shift needs to be opened.")
                return None
            
            # Handle unexpected status codes
            logger.error(f"Unexpected status code: {stat}")
            return None
        
        except Exception as e:
            logger.error(f"Failed to ensure open shift: {str(e)}")
            return None
        
    def open_new_shift(self):
        try:
            op_shift = open_shift_xml()
            status_code, shift_detail = self.shift_api.open_shift_api(op_shift)
            _, shift_id, _ = open_shift_response(shift_detail)
            logger.info(f"New shift {shift_id} opened.")
            return shift_id
        except Exception as e:
            logger.error(f"Failed to open new shift: {str(e)}",  )
            return None
    
    def close_shift(self, shift_id, popup):
        try:
            logger.info(f"Closing shift {shift_id}...")
            popup.update_status("Closing shift...")
            data_close = close_shift_xml(shift_id, "Closed")
            status_code, shift_detail = self.shift_api.close_shift_api(shift_id, data_close)

            if status_code == 200:
                logger.info(f"Closed Shift ID {shift_id} successfully")
            else:
                logger.error(f"Failed to close Shift ID {shift_id}. Status code: {status_code}")
        except Exception as e:
            logger.error(f"Failed to close shift: {str(e)}",  )
            raise
# -----------------------------------------------------------------------------------------------------------------
        

   
    
# ------------------------------- Footer Frame -----------------------------------------

    def create_footer_frame(self):
        self.version = self.get_version()
        
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.grid(row=2, column=0, sticky="ew")
        footer_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(footer_frame, text=f"Version {self.version} BETA", text_color=self.text_color, corner_radius=8).grid(row=0, column=0, sticky="e")
        ctk.CTkLabel(footer_frame, text="Asteroidea © 2024", text_color=self.text_color, corner_radius=8).grid(row=0, column=0, sticky="w")   
        
        link_button = ctk.CTkButton(footer_frame, text="Asteroidea © 2024", fg_color="transparent", text_color=self.text_color, hover_color=("gray70", "gray30"), border_width=0, cursor="hand2", command=self.open_link)
        link_button.grid(row=0, column=0, sticky="w") 
        
    def open_link(self):
        import webbrowser
        webbrowser.open("https://asteroidea.co/")  
        
    def get_version(self):
            try:
                with open('version.txt', 'r') as file:
                    version = file.read().strip()
                return version
            except FileNotFoundError:
                return "1.2.6"    
# --------------------------------------------------------------------------------------



# ------------------------------- Closing Shift Test -----------------------------------
    #def force_close_shift(self):
        #import webbrowser
        #webbrowser.open("https://asteroidea.co/")  
# --------------------------------------------------------------------------------------


