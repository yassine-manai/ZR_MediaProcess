import customtkinter as ctk

class TipsPopup(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Tips and Instructions")
        self.geometry("990x600")
        self.resizable(False, False)
        
        self.create_blurred_overlay()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(main_frame, text="Welcome to PAYG Import Tool", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10))
        
        tips_text = ctk.CTkTextbox(main_frame, width=560, height=270, fg_color="transparent", font=("Arial", 15))
        tips_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        tips_text.insert("1.0", """
                     
Tips and Instructions: 


            "Step 1:    Launch the application and review these instructions.",
            "Step 2:    Click on (Configuration) to config and check connection to ZR server and save it ",
            "Step 3:    Click on (Browse) to select your PAYG data file (CSV).",
            "Step 4:    Check if your date format is the same as the date format in the file",
            "Step 5:    If you check the (PMVC Topup) make sure that the file contain Amount values without (, / . / any special characters)",
            "Step 6:    Verify that all templates values are the same in the ZR server.",
            "Step 7:    If your file contain headers keep the (No Header) Checkbox unchecked , if not checked it",
            "Step 8:    Verify that all mandatory columns are present in your file",
            "Step 9:    If you like to add optional fields, add the field name and the header that match you header file with the (+) button",
            "Step 10:   If you like to remove an Optional field you can use the (x) button to remove the field",
            "Step 6:    Click 'Validate Data' to check for any errors or inconsistencies.",
            "Step 7:    Review the validation results and make any necessary corrections to your data.",
            "Step 8:    Once validation is successful, click (Start Process) to begin the import process.",
            "Step 9:    Monitor the import progress and wait for the completion message.",
            "Step 10:   After import, verify the imported data in the system to ensure accuracy."

                                                                
                                                                
------------------------------------------------------------------  Enjoy using the PAYG Import Tool! ------------------------------------------------------------------
        """)
        tips_text.configure(state="disabled")
        
        self.agree_var = ctk.BooleanVar()
        self.agree_checkbox = ctk.CTkCheckBox(main_frame, text="I have read and understood the instructions", variable=self.agree_var, command=self.update_button)
        self.agree_checkbox.grid(row=2, column=0, pady=(0, 10))
        
        self.continue_button = ctk.CTkButton(main_frame, text="Continue", command=self.on_continue)
        self.continue_button.grid(row=3, column=0, pady=(0, 10))
        
    def update_button(self):
        if self.agree_var.get():
            self.continue_button.configure(text="Continue", fg_color=["#3a7ebf", "#1f538d"])  # Default blue color
        else:
            self.continue_button.configure(text="Please agree to the instructions", fg_color="red")
    
    def on_continue(self):
        if self.agree_var.get():
            self.destroy()
            self.master.open_configuration()
        else:
            self.continue_button.configure(text="Please agree to the instructions", fg_color="red")

    def create_blurred_overlay(self):
        self.overlay = ctk.CTkFrame(self, fg_color="gray26")
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.overlay.configure(corner_radius=0)