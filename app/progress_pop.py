import customtkinter as ctk
from tkinter import messagebox

class ProcessingPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Processing Data")
        self.geometry("400x400")
        self.resizable(False, False)
        self.attributes('-topmost', True)  # Keep the popup on top

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create text widget
        self.text_widget = ctk.CTkTextbox(self, wrap="word", height=300, width=550, font=("Arial", 14))
        self.text_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create OK button
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy, font=("Arial", 14), height=40)
        self.ok_button.grid(row=1, column=0, pady=10)
        self.ok_button.configure(state="disabled")

    def update_status(self, message):
        self.text_widget.insert("end", message + "\n")
        self.text_widget.see("end")
        self.update()

    def enable_ok_button(self):
        self.ok_button.configure(state="normal")

    def show_error(self, error_message):
        messagebox.showerror("Error", error_message, parent=self)