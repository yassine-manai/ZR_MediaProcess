import customtkinter as ctk



class ProcessingPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Processing Data")
        self.geometry("800x400")
        self.resizable(False, False)
        self.attributes('-topmost', True)

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create text widget
        self.text_widget = ctk.CTkTextbox(self, wrap="word", height=300, width=550, font=("Arial", 14))
        self.text_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create OK button
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy, font=("Arial", 14), height=40)
        self.ok_button.grid(row=1, column=0, pady=10)
        self.ok_button.configure(state="disabled")  # Initially disabled

    def update_status(self, message):
        self.text_widget.insert("end", message + "\n")
        self.text_widget.see("end")
        self.update()

    def enable_ok_button(self):
        self.ok_button.configure(state="normal")

    def show_error(self, error_message):
        formatted_message = self.format_message(error_message, "❌")
        self.update_status(formatted_message)
        self.enable_ok_button()

    def show_success(self, success_message):
        formatted_message = self.format_message(success_message, "✔️")
        self.update_status(formatted_message)
        self.enable_ok_button()

    def format_message(self, message, icon, width=70):
        """Formats the message to align the icon at the end."""
        icon_position = width - len(icon) - 1  # Position for the icon
        padded_message = message.ljust(icon_position)  # Left-justify the message
        return f"{padded_message} {icon}\n"

