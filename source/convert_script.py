from pytube import *
from moviepy.editor import *
from tkinter import *
from tkinter import ttk
import shutil
import tkinter.messagebox as mbox
import os
import re
import traceback
import threading
import addition_script as adds
from time import sleep


def check_availability(asset):
    try:
        print(asset.vid_info)
        print()
        print(asset.streaming_data)
    except KeyError:
        mbox.showerror("System Error", "Video is unavailable now, please try again later")


def replace_unsupported_char(string):
    if re.search('[/\\"*|?:<>]', string, re.UNICODE):
        string = re.sub(r'[/\\"*|?:<>]', "", string)
    return string


def folder_sorting(folder_name, folder_dir):
    result_folder_name = None
    for fn in os.listdir(folder_dir):
        if re.search(re.escape(folder_name), fn):
            result_folder_name = fn + " - Copy"
        if result_folder_name is not None:
            if re.search(re.escape(result_folder_name), fn):
                result_folder_name += " - Copy"
    if result_folder_name is None:
        result_folder_name = folder_name
    direct = folder_dir + "/" + result_folder_name
    os.mkdir(direct)
    return direct


def file_sorting(asset, filedir, file_name, ext, ign):
    result_file_name = None
    for filename in os.listdir(filedir):
        if "." in filename:
            filename, file_ext = filename.rsplit(".", 1)
        if re.search(re.escape(file_name), filename):
            result_file_name = filename + " - Copy"
        if result_file_name is not None:
            if re.search(re.escape(result_file_name), filename):
                result_file_name += " - Copy"
    if result_file_name is None:
        result_file_name = file_name
    if ext == ".mp3":
        asset.download("Audio/Temp_MP4_files", filename=result_file_name + ".mp4")
        temp_mp4_file = f'Audio/Temp_MP4_files/{result_file_name}.mp4'
        new_mp3_file = f'{filedir}/{result_file_name}.mp3'
        video_file = VideoFileClip(temp_mp4_file)
        extracted_audio = video_file.audio
        extracted_audio.write_audiofile(new_mp3_file, codec="mp3")
        video_file.close()
        os.remove(temp_mp4_file)
    else:
        asset.download(filedir, filename=result_file_name + ext)
    if not ign:
        print("Download Successful!")
        mbox.showinfo("System", "Your conversion is successfully completed!")


def one_download(link, mode, directory, root):
    sync_event = threading.Event()
    stop_flag = threading.Event()
    max_percentage = 1000

    progression = DoubleVar()
    progressText = StringVar()
    loading = Toplevel(root)
    loading.title("YouTube Converter")
    loading.iconbitmap("icon.ico")
    loading.resizable(FALSE, FALSE)
    loading.protocol("WM_DELETE_WINDOW", lambda: None)
    loading.geometry(adds.sizing_positioning((1000, 200), adds.win_center_pos(loading, (1000,200))))
    root.attributes("-disabled", True)
    body = Frame(loading)
    progressionText = Label(body, textvariable=progressText, font=('Arial', 15))
    progressionBar = ttk.Progressbar(body, variable=progression, maximum=max_percentage)
    progressionText.grid(row=0, column=0, pady=(30, 10))
    progressionBar.grid(row=1, column=0, pady=(20, 60), padx=100, sticky=EW)
    body.grid_columnconfigure(0, weight=1)
    body.grid_rowconfigure(0, weight=1)
    body.pack(fill="both", expand=True)

    def fake_progressing(exceptional_percentage):
        def body():
            while not stop_flag.is_set():
                progression.set(progression.get() + 1)
                if progression.get() == exceptional_percentage: break
                sleep(0.05)
            sleep(1)
            return
        fp = threading.Thread(target=body)
        fp.start()

    def raiseErr(errCode):
        global err_code
        loading.destroy()
        root.attributes("-disabled", False)
        err_code = errCode
        sync_event.set()
    
    def real_progressing(showingTask, progress, holdingTime, job, kwargs=None):
        stop_flag.clear()
        progressText.set(showingTask)
        fake_progressing(progress)
        job(kwargs)
        sleep(holdingTime)
        stop_flag.set()
        progression.set(progress)

    def work(): 
        global f
        global video
        try:
            def retrieve_link(*args, **kwargs): 
                global f
                f = YouTube(link)
            real_progressing("Retrieving YouTube link...", 100, 2, retrieve_link)
        except Exception:
            raiseErr("001")
            return

        if directory == "": 
            raiseErr("002")
            return

        output_ext = None
        if mode.lower() == "video":
            output_ext = ".mp4"
        elif mode.lower() == "audio":
            output_ext = ".mp3"
        try:
            def get_video(yt_v):
                global video
                check_availability(yt_v)
                video = f.streams.get_highest_resolution()
            real_progressing("Check for the video availability...", 200, 4, get_video, {'yt_v': f})
        except: 
            raiseErr("003")
            return

        # try:
        #     file_dir = directory
        #     f.title = replace_unsupported_char(f.title)
        #     file_sorting(video, file_dir, f.title, output_ext, False)
        #     # progressionBar.pack()
        #     # progressionText.pack()
        # except WindowsError:
        #     print("File's name doesn't support, but it downloaded successful anyway.")
        #     mbox.showwarning("System Warning", "File's name doesn't support, your file has been downloaded! (Code: 3009)")
        # except FileExistsError:
        #     print("The file is already exist!")
        #     mbox.showerror("System Error", "The file is already exist!")
        # except PermissionError:
        #     print("You don't have permission to download into this folder")
        #     mbox.showerror("System Error", "You don't have permission to download into this folder!")
        # except Exception as e:
        #     traceback_str = traceback.format_exc()
        #     print("An Error occurred")
        #     mbox.showerror("System Error", "An unknown error occurred!")
        #     mbox.showerror("System Error", "Detail: " + str(e) if e is not None else "No error details available.")
        #     mbox.showerror("System Error", f"{traceback_str}")

    def catch_error():
        global err_code
        sync_event.wait()
        while err_code:
            if err_code == "001": 
                mbox.showerror("System Error", f"Invalid YouTube Link! (Error Code: {err_code})")
                break
            elif err_code == "002": 
                mbox.showerror("System Error", f"Invalid File Path! (Error Code: {err_code})")
                break
            elif err_code == "003":
                mbox.showerror("System Error", f"The video is currently unavailable, We're sorry about that! (Error Code: {err_code})")
                break
        else: mbox.showinfo("System", "Your conversion is successfully completed!")
    
    convert = threading.Thread(target=work)
    convert.start()
    catch = threading.Thread(target=catch_error)
    catch.start()


def playlist_download(link, mode, pldir):
    playlist = None
    if re.search("playlist", link):
        playlist = Playlist(link)
    else:
        mbox.showerror("System Error", "Invalid YouTube Link!")
        return
    if pldir == "":
        mbox.showerror("System Error", "Invalid File Path!")
        return
    output_ext = None
    if mode.lower() == "video":
        output_ext = ".mp4"
    elif mode.lower() == "audio":
        output_ext = ".mp3"
    dir = folder_sorting(replace_unsupported_char(playlist.title), pldir)
    success = True
    for v in playlist.videos:
        try:
            check_availability(v)
            video = v.streams.get_highest_resolution()
            v.title = replace_unsupported_char(v.title)
            file_sorting(video, dir, v.title, output_ext, True)
        except WindowsError:
            print("File's name doesn't support, but it downloaded successful anyway.")
            mbox.showwarning("System Warning", "File's name doesn't support, your file has been downloaded! (Code: 3009)")
        except FileExistsError:
            print("The file is already exist!")
            mbox.showerror("System Error", "The file is already exist!")
            shutil.rmtree(dir, ignore_errors=True)
            success = False
            break
        except PermissionError:
            print("You don't have permission to download into this folder")
            mbox.showerror("System Error", "You don't have permission to download into this folder!")
            shutil.rmtree(dir, ignore_errors=True)
            success = False
            break
        except Exception as e:
            traceback_str = traceback.format_exc()
            print("An Error occurred")
            mbox.showerror("System Error", "An unknown error occurred!")
            mbox.showerror("System Error", "Detail: " + str(e) if e is not None else "No error details available.")
            mbox.showerror("System Error", f"{traceback_str}")
            shutil.rmtree(dir, ignore_errors=True)
            success = False
            break
    if success:
        print("Download Successful!")
        mbox.showinfo("System", "Your conversion is successfully completed!")
