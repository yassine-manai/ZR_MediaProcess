from tkinter import ttk
import customtkinter as ctk

class ProgressPopup(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Processing Progress")
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.steps = [
            "Reading CSV file",
            "Validating data",
            "Testing ZR connection",
            "Processing companies",
            "Processing participants"
        ]

        self.progress_bars = {}
        self.status_labels = {}

        for i, step in enumerate(self.steps):
            label = ctk.CTkLabel(self.main_frame, text=step)
            label.grid(row=i*2, column=0, padx=5, pady=5, sticky="w")

            progress_bar = ttk.Progressbar(self.main_frame, mode="indeterminate", length=200)
            progress_bar.grid(row=i*2+1, column=0, padx=5, pady=5, sticky="ew")

            status_label = ctk.CTkLabel(self.main_frame, text="")
            status_label.grid(row=i*2, column=1, padx=5, pady=5, sticky="e")

            self.progress_bars[step] = progress_bar
            self.status_labels[step] = status_label

    def start_progress(self, step):
        self.progress_bars[step].start()

    def stop_progress(self, step, status):
        self.progress_bars[step].stop()
        self.status_labels[step].configure(text="✓" if status else "✗")