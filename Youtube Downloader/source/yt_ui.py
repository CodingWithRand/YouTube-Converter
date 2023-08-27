from tkinter.ttk import Combobox
from tkinter import *
from tkinter.filedialog import *
from convert_script import *
import tkinter.messagebox as mbox
import re

# UI Addition Functions

selection = None

def return_selectopt(event):
    global selection
    selection = event.widget.get()

def dircustomize(_mode, defaultdirtext):
    # Fix here
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


def dirsection2(p, of, defaultdirtext, mode):
    # Browse Dir
    dirc = Frame(p)
    Label(dirc, text="Directory", font=of).grid(column=0, row=0)
    Entry(dirc, textvariable=defaultdirtext, state="disabled").grid(column=1, row=0, ipadx=55)

    Button(dirc, text="Browse", bg="white", activebackground="lightgrey", command=lambda: dircustomize(mode, defaultdirtext)).grid(column=2, row=0, ipadx=10)
    dirc.pack(pady=(10, 0))


def convert(mode, entry, dir):
    if re.search("Playlist", mode.get()):
        if re.search("Video", mode.get()):
            playlist_download(entry.get(), "Video", dir)
        elif re.search("Audio", mode.get()):
            playlist_download(entry.get(), "Audio", dir)
    elif mode.get() == "Select Option":
        mbox.showerror("System Error", "Please select a valid conversion!")
    else:
        one_download(entry.get(), mode.get(), dir)


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

def Constructed_UI2(window, of, defaultdirtext, selectoption, opt):
    # Head

    Label(window, text="Youtube Converter", font=("Comic Sans MS", 50), fg="red").pack(ipady=10, ipadx=100)

    # Convert section

    desc = Label(window, text="All kind of conversion available (Video, Audio, and Playlist)", font=("Arial Rounded MT Bold", 20))
    desc.pack(ipady=20)
    option = Combobox(window, textvariable=selectoption, values=opt, state='readonly', width=33, font=of)
    option.pack(pady=(10, 5))
    option.current(0)
    option.bind("<<ComboboxSelected>>", return_selectopt)
    file = Entry(window, font=of, fg="grey")
    file.insert(0, "YouTube Link here")

    focus = bindFocus(file, "YouTube Link here")

    file.bind("<FocusIn>", focus.on_focusin)
    file.bind("<FocusOut>", focus.on_focusout)

    file.pack(ipadx=80)
    dirsection2(window, of, defaultdirtext, selectoption.get())
    Button(window, font=of, text="Convert & Download ", bg="white", activebackground="lightgrey",
                command=lambda: convert(selectoption, file, defaultdirtext.get())).pack(ipadx=40, pady=(10, 20))

    window.mainloop()