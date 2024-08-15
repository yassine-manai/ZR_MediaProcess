import threading
import customtkinter as ctk

def create_loading_popup(parent, message="Loading...", timer=None):
    loading_popup = ctk.CTkToplevel(parent)
    loading_popup.title("Loading")
    loading_popup.geometry("300x100")  
    loading_popup.resizable(False, False)  
    
    # Center the popup on the screen
    loading_popup.update_idletasks()
    x = (loading_popup.winfo_screenwidth() // 2) - (loading_popup.winfo_width() // 2)
    y = (loading_popup.winfo_screenheight() // 2) - (loading_popup.winfo_height() // 2)
    loading_popup.geometry(f'+{x}+{y}')
    
    # Create a frame inside the popup
    loading_frame = ctk.CTkFrame(loading_popup)
    loading_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Add a loading label
    loading_label = ctk.CTkLabel(loading_frame, text=message, font=("Arial", 14))
    loading_label.pack(pady=10)

    # Optionally, add a progress bar or spinner
    progress_bar = ctk.CTkProgressBar(loading_frame, mode="indeterminate")
    progress_bar.pack(fill="x", pady=10)
    progress_bar.start()

    # This will make the popup modal (blocks interaction with other windows)
    loading_popup.transient(parent)
    loading_popup.grab_set()

    # If a timer is specified, close the popup after the specified time
    if timer:
        threading.Timer(timer, lambda: close_loading_popup(loading_popup)).start()

    return loading_popup

def close_loading_popup(loading_popup):
    if loading_popup:
        loading_popup.destroy()

def show_loading_popup(parent, message="Loading...", timer=None):
    popup = create_loading_popup(parent, message, timer)
    parent.wait_window(popup)