from pytube import *
from moviepy.editor import *
from tkinter import *
from time import sleep
from tkinter import messagebox as mbox
import shutil
import os
import re
import traceback
import threading

def check_availability(asset):
    try:
        print(asset.vid_info)
        print()
        print(asset.streaming_data)
    except KeyError:
        mbox.showerror("System Error", "Video is unavailable now, please try again later")


def replace_unsupported_char(string):
    if re.search(r'[/\\"*|?:<>]', string, re.UNICODE):
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


def file_sorting(asset, filedir, file_name, ext):
    result_file_name = None
    for filename in os.listdir(filedir):
        if "." in filename:
            filename, file_ext = filename.rsplit(".", 1)
        if re.search(re.escape(file_name), filename):
            print(re.search(re.escape(file_name), filename), re.escape(file_name), filename)
            result_file_name = filename + " - Copy"
            print(result_file_name)
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


def one_download(link, mode, directory, root):
    sync_event = threading.Event()
    stop_flag = {
        "fp": threading.Event(),
        "work": threading.Event(),
        "catch-err": threading.Event()
    }
    max_percentage = 1000

    progression = DoubleVar()
    progressText = StringVar()
    

    UI = __import__('yt_ui')
    UI.loading_progress(root, progressText, progression, max_percentage)

    def fake_progressing(exceptional_percentage):
        def body():
            if not stop_flag["fp"].is_set():
                for _ in range(int(progression.get()), exceptional_percentage):
                    if progression.get() == exceptional_percentage: 
                        print("thread stop")
                        break
                    progression.set(progression.get() + 1)
                    sleep(0.05)
            return
        fp = threading.Thread(target=body)
        fp.daemon = True
        fp.start()

    def raiseErr(errCode):
        global err_code
        UI.loading.destroy()
        root.attributes("-disabled", False)
        err_code = errCode
        stop_flag["work"].set()
        sync_event.set()
    
    def real_progressing(showingTask, progress, holdingTime, job, kwargs=None):
        stop_flag["fp"].clear()
        progressText.set(showingTask)
        fake_progressing(progress)
        if kwargs is not None: job(**kwargs)
        else: job()
        sleep(holdingTime)
        stop_flag["fp"].set()
        progression.set(progress)

    def work():
        global f
        global video
        global output_ext
        global err_code
        if not stop_flag["work"].is_set():
            try:
                def retrieve_link(): 
                    global f
                    f = YouTube(link)
                real_progressing("Retrieving YouTube link...", 100, 2, retrieve_link)
            except Exception:
                raiseErr("1404")
                # raise Exception
                return

            if directory == "": 
                raiseErr("2404")
                # raise Exception("Please provide file path!")
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
                real_progressing("Check for the video availability...", 200, 2, get_video, {'yt_v': f})
            except Exception: 
                raiseErr("3150")
                # raise Exception
                return

            try:
                def download_video(vid, vidTitle):
                    global output_ext
                    file_dir = directory
                    vidTitle = replace_unsupported_char(vidTitle)
                    file_sorting(vid, file_dir, vidTitle, output_ext)
                real_progressing(f"Downloading the {mode.lower()}...", 1000, 1, download_video, {'vid': video, 'vidTitle': f.title})
                UI.loading.destroy()
                root.attributes("-disabled", False)
            except WindowsError:
                raiseErr("3009")
                # raise WindowsError
                return
            except FileExistsError:
                raiseErr("0058")
                # raise FileExistsError
                return
            except PermissionError:
                raiseErr("4003")
                # raise PermissionError
                return
            except Exception as e:
                traceback_str = traceback.format_exc()
                raiseErr("9999")
                mbox.showerror("System Error", f"{traceback_str}")
                # raise e
                return

        err_code = None
        return

    def catch_error():
        global err_code
        sync_event.wait()
        if not stop_flag["catch-err"].is_set():
            if err_code:
                if err_code == "1404": mbox.showerror("System Error", f"Invalid YouTube Link! (Error Code: {err_code})")
                elif err_code == "2404": mbox.showerror("System Error", f"Invalid File Path! (Error Code: {err_code})")
                elif err_code == "3150": mbox.showerror("System Error", f"The video is currently unavailable, We're sorry about that! (Error Code: {err_code})")
                elif err_code == "3009": mbox.showwarning("System Warning", f"File's name doesn't support, your file has been downloaded! (Warning Code: {err_code})")
                elif err_code == "0058": mbox.showerror("System Error", f"The file is already exist! (Error Code: {err_code})")
                elif err_code == "4003": mbox.showerror("System Error", f"You don't have permission to download into this folder! (Error Code: {err_code})")
                elif err_code == "9999": mbox.showerror("System Error", f"An unknown error occurred! (Error Code: {err_code})")
            else: 
                mbox.showinfo("System", "Your conversion is successfully completed!")
                
        stop_flag["catch-err"].set()
        stop_flag["work"].set()
        stop_flag["fp"].set()
        sync_event.set()
        return
    
    convert = threading.Thread(target=work)
    convert.daemon = True
    convert.start()
    catch = threading.Thread(target=catch_error)
    catch.daemon = True
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
            file_sorting(video, dir, v.title, output_ext)
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
