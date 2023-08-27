# Converter Functions
from convert_script import *
# UI Functions
import yt_ui
from tkinter import *

import os

if not os.path.exists("Video"):
    os.mkdir("Video")
if not os.path.exists("Audio"):
    os.mkdir("Audio")
if not os.path.exists("Playlist"):
    os.mkdir("Playlist")
    os.mkdir("Playlist/Videos")
    os.mkdir("Playlist/Audios")
else:
    if not os.path.exists("Playlist/Videos"):
        os.mkdir("Playlist/Videos")
    elif not os.path.exists("Playlist/Audios"):
        os.mkdir("Playlist/Audios")

window = Tk()
window.title("Youtube Converter")
window.resizable(FALSE, FALSE)
window.iconbitmap("icon.ico")

# Variable
originfont = ("Arial", 15)
opt = ["Select Option", "Video", "Audio", "Playlist (Video)", "Playlist (Audio)"]
defaultdirtext = StringVar()
selectoption = StringVar()

yt_ui.Constructed_UI2(window, originfont, defaultdirtext, selectoption, opt)

# title = ""
# counter = 1
#
# while True:
#     l = input("Enter the youtube video url link: ")
#     m = input("Video or Audio ")
#
#     if l == "": break
#     elif l == "playlist":
#         pl = input("Enter the playlist url link: ")
#         playlist_download(pl, m)
#
#     file_name = YouTube(l).title
#     if file_name != title:
#         one_download(l, m, "Audio")
#         title = file_name
#     else:
#         file_name = file_name, "(%d)" % counter
#         one_download(l, m, file_name)
#         counter += 1
