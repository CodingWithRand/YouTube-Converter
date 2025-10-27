from tkinter.ttk import Combobox, Progressbar
from tkinter import *
from tkinter.filedialog import *
from convert_script import one_download, playlist_download
import tkinter.messagebox as mbox
import re
import addition_script as adds


# UI Addition Functions

originfont = ("Arial", 15)
conversion_selection = None

def loading_progress(root, progressText, progression, max_percentage):
    global loading
    loading = Toplevel(root)
    loading.title("YouTube Converter")
    loading.iconbitmap("icon.ico")
    loading.resizable(FALSE, FALSE)
    loading.protocol("WM_DELETE_WINDOW", lambda: None)
    loading.geometry(adds.sizing_positioning((1000, 200), adds.win_center_pos(loading, (1000,200))))
    root.attributes("-disabled", True)
    body = Frame(loading)
    progressionText = Label(body, textvariable=progressText, font=originfont)
    progressionBar = Progressbar(body, variable=progression, maximum=max_percentage)
    progressionText.grid(row=0, column=0, pady=(30, 10))
    progressionBar.grid(row=1, column=0, pady=(20, 60), padx=100, sticky=EW)
    body.grid_columnconfigure(0, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.pack(fill="both", expand=True)

def show_notification(title, message, root):
    notification = Toplevel(root)
    notification.title(title)
    notification.geometry("300x100")
    notification.attributes("-topmost", True)  # Bring the notification to the front
    notification.resizable(False, False)

    label = Label(notification, text=message, font=originfont)
    label.pack(pady=20)

    ok_button = Button(notification, text="OK", command=notification.destroy)
    ok_button.pack()

def return_conversion_selectopt(event, res_option):
    global conversion_selection
    conversion_selection = event.widget.get()
    if conversion_selection == "Video" or conversion_selection == "Playlist (Video)":
        res_option.grid(row=1, column=0, pady=(0,5))
    else:
        res_option.grid_remove()


def return_res_selectopt(event):
    global res_selection
    res_selection = event.widget.get()

def dircustomize(defaultdirtext):
    global conversion_selection
    if conversion_selection is not None:
        directory = askdirectory()
        if directory == "":
            return 0
        else:
            defaultdirtext.set(directory)
    else:
        mbox.showwarning("System Warning", "Please select the conversion type first!")


def dirsection2(p, defaultdirtext):
    # Browse Dir
    dirc = Frame(p)
    Label(dirc, text="Directory", font=originfont).grid(column=0, row=0)
    Entry(dirc, textvariable=defaultdirtext, state="disabled").grid(column=1, row=0, ipadx=55)

    Button(dirc, text="Browse", bg="white", activebackground="lightgrey", command=lambda: dircustomize(defaultdirtext)).grid(column=2, row=0, ipadx=10)
    dirc.pack(pady=(10, 0))


def convert(mode, entry, res, dir, window):
    if re.search("Playlist", mode.get()):
        if re.search("Video", mode.get()):
            if res.get() == "Select Resolution":
                mbox.showerror("System Error", "Please select a valid resolution!")
            else:
                playlist_download(entry.get(), "Video", res.get(), dir, window)
        elif re.search("Audio", mode.get()):
            playlist_download(entry.get(), "Audio", res.get(), dir, window)
    elif mode.get() == "Video":
        if res.get() == "Select Resolution":
            mbox.showerror("System Error", "Please select a valid resolution!")
        else:
            one_download(entry.get(), "Video", res.get(), dir, window)
    elif mode.get() == "Audio":
        one_download(entry.get(), "Audio", res.get(), dir, window)
    elif mode.get() == "Select Option":
        mbox.showerror("System Error", "Please select a valid conversion!")


class bindFocus:
    def __init__(self, entry, text):
        self.entrybox = entry
        self.sorttext = text

    def on_focusin(self, event=None):
        if self.entrybox.get() == self.sorttext:
            self.entrybox.delete(0, END)
            self.entrybox.config(fg='black')

    def on_focusout(self, event=None):
        if self.entrybox.get() == '':
            self.entrybox.insert(0, self.sorttext)
            self.entrybox.config(fg='grey')


# UI Main Functions

def Constructed_UI2(window: Tk, defaultdirtext, conversion_selected_option, conversion_opts, res_selected_option, res_opts):
    # Head

    Label(window, text="Youtube Converter", font=("Comic Sans MS", 50), fg="red").pack(ipady=10, ipadx=100)

    # Convert section

    # window.protocol("WM_DELETE_WINDOW", adds.print_thread_status) - Debug

    desc = Label(window, text="All kind of conversion available (Video, Audio, and Playlist)", font=("Arial Rounded MT Bold", 20))
    desc.pack(ipady=20)

    selection_frame = Frame(window)
    selection_frame.pack()

    conversion_option = Combobox(selection_frame, textvariable=conversion_selected_option, values=conversion_opts, state='readonly', width=33, font=originfont)
    conversion_option.current(0)
    conversion_option.bind("<<ComboboxSelected>>", lambda event: return_conversion_selectopt(event, res_option))
    conversion_option.grid(row=0, column=0, pady=(0,5))
    
    res_option = Combobox(selection_frame, textvariable=res_selected_option, values=res_opts, state='readonly', width=33, font=originfont)
    res_option.current(0)
    res_option.bind("<<ComboboxSelected>>", return_res_selectopt)

    file = Entry(window, font=originfont, fg="grey")
    file.insert(0, "YouTube Link here")

    focus = bindFocus(file, "YouTube Link here")

    file.bind("<FocusIn>", focus.on_focusin)
    file.bind("<FocusOut>", focus.on_focusout)

    file.pack(ipadx=80)
    dirsection2(window, defaultdirtext)
    Button(window, font=originfont, text="Convert & Download ", bg="white", activebackground="lightgrey",
                command=lambda: convert(conversion_selected_option, file, res_selected_option, defaultdirtext.get(), window)).pack(ipadx=40, pady=(10, 20))

    window.mainloop()