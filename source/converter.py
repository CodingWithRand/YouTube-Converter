# Converter Functions
from convert_script import *
# UI Functions
from yt_ui import Constructed_UI2
from tkinter import *
import addition_script as adds

window = Tk()
window.title("YouTube Converter v1.5.2")
window.resizable(FALSE, FALSE)
window.geometry(adds.sizing_positioning((800, 400), adds.win_center_pos(window, (800, 400))))
window.iconbitmap("icon.ico")

# Variable
conversion_opts = ["Select Conversion Option", "Video", "Audio", "Playlist (Video)", "Playlist (Audio)"]
res_opts = ["Select Resolution", "144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]

defaultdirtext = StringVar()
conversion_selected_option = StringVar()
res_selected_option = StringVar()

Constructed_UI2(window, defaultdirtext, conversion_selected_option, conversion_opts, res_selected_option, res_opts)

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
