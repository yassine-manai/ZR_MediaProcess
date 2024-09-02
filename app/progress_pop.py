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
        self.text_widget.configure(state="disabled")
        self.text_widget.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Create progress bar
        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate", width=550)
        self.progress_bar.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)  # Initial progress set to 0%

        # Create percentage label
        self.percentage_label = ctk.CTkLabel(self, text="0%", font=("Arial", 12))
        self.percentage_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="e")

        # Create OK button
        self.ok_button = ctk.CTkButton(self, text="OK", command=self.destroy, font=("Arial", 14), height=40)
        self.ok_button.grid(row=3, column=0, pady=10)
        self.ok_button.configure(state="disabled")  # Initially disabled

    def update_status(self, message):
        if self.winfo_exists():  # Check if the widget exists
            self.text_widget.configure(state="normal")
            self.text_widget.insert("end", message + "\n")
            self.text_widget.see("end")
            self.text_widget.configure(state="disabled")
            self.update()
        else:
            print("Attempted to update a destroyed widget.")

    def enable_ok_button(self):
        self.ok_button.configure(state="normal")

    def show_error(self, error_message):
        self.text_widget.configure(state="normal")
        formatted_message = self.format_message(error_message, "❌")
        self.update_status(formatted_message)
        self.text_widget.configure(state="disabled")
        self.enable_ok_button()

    def show_success(self, success_message):
        formatted_message = self.format_message(success_message, "✔️")
        self.update_status(formatted_message)
        self.enable_ok_button()

    def format_message(self, message, icon, width=70):
        """Formats the message to align the icon at the end."""
        icon_position = width - len(icon) - 1  # Position for the icon
        padded_message = message.ljust(icon_position)
        return f"{padded_message} ------------------------------------ {icon} \n"

    def update_progress(self, progress):
        """Updates the progress bar and percentage label."""
        self.progress_bar.set(progress / 100.0)  
        self.percentage_label.configure(text=f"{progress}%")  # Update the percentage label
        self.update()  

