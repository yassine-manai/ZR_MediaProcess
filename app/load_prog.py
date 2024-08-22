import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import threading
import time
import math

class LoadingDialog(tk.Toplevel):
    def __init__(self, parent, message="Loading..."):
        super().__init__(parent)
        self.title("Please Wait")
        self.geometry("300x200")
        self.resizable(False, False)
        self.grab_set()

        self.label = ttk.Label(self, text=message, font=("Arial", 14))
        self.label.pack(pady=20)

        self.canvas = tk.Canvas(self, width=100, height=100)
        self.canvas.pack()

        self.angle = 0
        self.arc = self.canvas.create_arc((10, 10, 90, 90), start=0, extent=150, style=tk.ARC, outline="blue", width=4)
        self.animate()

    def animate(self):
        self.angle += 10
        self.canvas.itemconfig(self.arc, start=self.angle)
        self.after(50, self.animate)

    def close(self):
        self.grab_release()
        self.destroy()

def show_loading_dialog(parent, message):
    loading_dialog = LoadingDialog(parent, message)
    parent.wait_window(loading_dialog)

def process_with_loading():
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Run the loading dialog in a separate thread
    threading.Thread(target=show_loading_dialog, args=(root, "Please wait, processing...")).start()

    # Simulate some long processing work
    time.sleep(5)  # Replace this with actual work

    # Show a completion message
    messagebox.showinfo("Done", "Processing completed successfully!")
    root.quit()