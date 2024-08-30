import customtkinter as ctk

class TipsPopup(ctk.CTkToplevel):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Tips and Instructions")
        self.geometry("990x600")
        self.resizable(False, False)
        
        # Configure grid for the entire window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Title label directly in self (TipsPopup window)
        title_label = ctk.CTkLabel(self, text="Welcome to PAYG Import Tool", font=("Arial", 18, "bold"))
        title_label.grid(row=0, column=0, pady=(10, 5), sticky="n")

        # Tips text box directly in self (TipsPopup window)
        tips_text = ctk.CTkTextbox(self, width=960, height=450, fg_color="transparent", font=("Arial", 15))
        tips_text.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="nsew")
        tips_text.insert("1.0", """
Tips and Instructions:

Step 1: Launch the application and review these instructions.
Step 2: Click on (Configuration) to configure and check connection to ZR server and save it.
Step 3: Click on (Browse) to select your PAYG data file (CSV).
Step 4: Check if your date format is the same as the date format in the file.
Step 5: If you check the (PMVC Topup) ensure that the file contains Amount values without commas, periods, or special characters.
Step 6: Verify that all template values are the same on the ZR server.

Step 7: If your file contains headers, keep the (No Header) Checkbox unchecked; if not, check it.

Step 8: Verify that all mandatory columns are present in your file.

Step 9: To add optional fields, add the field name and match it with the header in your file using the (+) button.

Step 10: To remove an optional field, use the (x) button.

Step 11: Click 'Validate Data' to check for errors or inconsistencies.

Step 12: Review the validation results and make necessary corrections to your data.

Step 13: Once validation is successful, click (Start Process) to begin the import.

Step 14: Monitor the import progress and wait for the completion message.

Step 15: After import, verify the data in the system for accuracy.





------------------------------------------------------------------  Enjoy using the PAYG Import Tool! ------------------------------------------------------------------
        """)
        tips_text.configure(state="disabled")

        # Agree checkbox directly in self (TipsPopup window)
        self.agree_var = ctk.BooleanVar()
        self.agree_checkbox = ctk.CTkCheckBox(self, text="I have read and understood the instructions", variable=self.agree_var, command=self.update_button)
        self.agree_checkbox.grid(row=2, column=0, pady=(10, 5), sticky="w", padx=10)

        # Continue button directly in self (TipsPopup window)
        self.continue_button = ctk.CTkButton(self, text="Continue", command=self.on_continue)
        self.continue_button.grid(row=3, column=0, pady=(5, 20))

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
