import customtkinter as ctk


class LoadingCircle(ctk.CTkCanvas):
    def __init__(self, master, size=20, fg_color="#1F6AA5", bg_color="#2B2B2B"):
        super().__init__(master, width=size, height=size, bg=bg_color, highlightthickness=0)
        self.size = size
        self.fg_color = fg_color
        self.angle = 0
        self.arc = None

    def start(self):
        self.draw()

    def draw(self):
        if self.arc:
            self.delete(self.arc)
        start = self.angle
        extent = 90
        x = y = self.size / 2
        self.arc = self.create_arc(0, 0, self.size, self.size, start=start, extent=extent, fill=self.fg_color, outline="")
        self.angle = (self.angle + 10) % 360
        self.after(50, self.draw)
