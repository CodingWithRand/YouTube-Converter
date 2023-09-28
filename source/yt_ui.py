from tkinter.ttk import Combobox, Progressbar
from tkinter import *
from tkinter.filedialog import *
from convert_script import one_download, playlist_download
import tkinter.messagebox as mbox
import re
import addition_script as adds


# UI Addition Functions

originfont = ("Arial", 15)
selection = None

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

def return_selectopt(event):
    global selection
    selection = event.widget.get()

def dircustomize(_mode, defaultdirtext):
    if selection is not None:
        directory = askdirectory()
        if selection == 'Video':
            if re.search('(video)$', directory, re.IGNORECASE):
                defaultdirtext.set("(Default)")
            elif directory == "":
                return 0
            else:
                defaultdirtext.set(directory)
        elif selection == 'Audio':
            if re.search('(audio)$', directory, re.IGNORECASE):
                defaultdirtext.set("(Default)")
            elif directory == "":
                return 0
            else:
                defaultdirtext.set(directory)
        elif _mode == 'Playlist (Video)':
            if re.search('(playlist)$', directory, re.IGNORECASE):
                defaultdirtext.set("(Default)")
            elif re.search('(playlist/videos)$', directory, re.IGNORECASE):
                defaultdirtext.set("(Default)/Videos")
            elif directory == "":
                return 0
            else:
                defaultdirtext.set(directory)
        elif _mode == 'Playlist (Audio)':
            if re.search('(playlist)$', directory, re.IGNORECASE):
                defaultdirtext.set("(Default)")
            elif re.search('(playlist/audios)$', directory, re.IGNORECASE):
                defaultdirtext.set("(Default)/Audios")
            elif directory == "":
                return 0
            else:
                defaultdirtext.set(directory)
        elif _mode == "Select Option":
            if directory == "":
                return 0
            else:
                defaultdirtext.set(directory)
    else:
        mbox.showwarning("System Warning", "Please select the conversion type first!")


def dirsection2(p, defaultdirtext, mode):
    # Browse Dir
    dirc = Frame(p)
    Label(dirc, text="Directory", font=originfont).grid(column=0, row=0)
    Entry(dirc, textvariable=defaultdirtext, state="disabled").grid(column=1, row=0, ipadx=55)

    Button(dirc, text="Browse", bg="white", activebackground="lightgrey", command=lambda: dircustomize(mode, defaultdirtext)).grid(column=2, row=0, ipadx=10)
    dirc.pack(pady=(10, 0))


def convert(mode, entry, dir, window):
    if re.search("Playlist", mode.get()):
        if re.search("Video", mode.get()):
            playlist_download(entry.get(), "Video", dir)
        elif re.search("Audio", mode.get()):
            playlist_download(entry.get(), "Audio", dir)
    elif mode.get() == "Select Option":
        mbox.showerror("System Error", "Please select a valid conversion!")
    else:
        one_download(entry.get(), mode.get(), dir, window)


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

def Constructed_UI2(window, defaultdirtext, selectoption, opt):
    # Head

    Label(window, text="Youtube Converter", font=("Comic Sans MS", 50), fg="red").pack(ipady=10, ipadx=100)

    # Convert section

    desc = Label(window, text="All kind of conversion available (Video, Audio, and Playlist)", font=("Arial Rounded MT Bold", 20))
    desc.pack(ipady=20)
    option = Combobox(window, textvariable=selectoption, values=opt, state='readonly', width=33, font=originfont)
    option.pack(pady=(10, 5))
    option.current(0)
    option.bind("<<ComboboxSelected>>", return_selectopt)
    file = Entry(window, font=originfont, fg="grey")
    file.insert(0, "YouTube Link here")

    focus = bindFocus(file, "YouTube Link here")

    file.bind("<FocusIn>", focus.on_focusin)
    file.bind("<FocusOut>", focus.on_focusout)

    file.pack(ipadx=80)
    dirsection2(window, defaultdirtext, selectoption.get())
    Button(window, font=originfont, text="Convert & Download ", bg="white", activebackground="lightgrey",
                command=lambda: convert(selectoption, file, defaultdirtext.get(), window)).pack(ipadx=40, pady=(10, 20))

    window.mainloop()