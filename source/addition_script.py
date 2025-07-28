from tkinter import *
from tkinter import font
import threading
import sys
import os

# Real Usage

def win_center_pos(window, win_size):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    pos = (int((screen_width/2) - (win_size[0]/2)), int((screen_height/2) - (win_size[1]/2)))
    return pos


def sizing_positioning(size, pos):
    return f"{size[0]}x{size[1]}+{pos[0]}+{pos[1]}"


# For debug

def print_thread_status():
    for thread in threading.enumerate():
        print(f"Thread Name: {thread.name}, Status: {'Alive' if thread.is_alive() else 'Not Alive'}")


def show_all_font_styles():
    # Create an instance of tkinter frame
    win = Tk()
    win.geometry("750x350")
    win.title('Font List')
    # Create a list of font using the font-family constructor
    fonts = list(font.families())
    fonts.sort()

    def fill_frame(frame):
        for f in fonts:
            # Create a label to display the font
            label = Label(frame, text=f, font=(f, 14)).pack()

    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Create a canvas
    canvas = Canvas(win, bd=1, background="white")
    # Create a frame inside the canvas
    frame = Frame(canvas, background="white")
    # Add a scrollbar
    scroll_y = Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", expand=1, fill="both")
    canvas.create_window((5, 4), window=frame, anchor="n")
    frame.bind("<Configure>", lambda e, canvas=canvas: onFrameConfigure(canvas))
    fill_frame(frame)
    win.mainloop()

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):  # Running in a PyInstaller bundle
        temp_dir = sys._MEIPASS
        return os.path.join(temp_dir, "ffmpeg.exe")
    else:  # Running in normal Python
        return os.path.join(os.path.dirname(__file__), "ffmpeg.exe")