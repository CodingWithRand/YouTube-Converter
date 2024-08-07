from pytubefix import *
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
        asset.vid_info
        asset.streaming_data
        # print(asset.vid_info)
        print()
        # print(asset.streaming_data)
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
                real_progressing(f"Checking for the {mode.lower()} availability...", 200, 2, get_video, {'yt_v': f})
            except Exception: 
                raiseErr("3150")
                raise Exception
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
        mbox.showinfo("System", "Your conversion is successfully completed!")
                
        stop_flag["catch-err"].set()
        stop_flag["work"].set()
        stop_flag["fp"].set()
        return

    def catch_error():
        global err_code
        sync_event.wait()
        if not stop_flag["catch-err"].is_set():
            if err_code is not None:
                if err_code == "1404": mbox.showerror("System Error", f"Invalid YouTube Link! (Error Code: {err_code})")
                elif err_code == "2404": mbox.showerror("System Error", f"Invalid File Path! (Error Code: {err_code})")
                elif err_code == "3150": mbox.showerror("System Error", f"The video is currently unavailable, We're sorry about that! (Error Code: {err_code})")
                elif err_code == "3009": mbox.showwarning("System Warning", f"File's name doesn't support, your file has been downloaded! (Warning Code: {err_code})")
                elif err_code == "0058": mbox.showerror("System Error", f"The file is already exist! (Error Code: {err_code})")
                elif err_code == "4003": mbox.showerror("System Error", f"You don't have permission to download into this folder! (Error Code: {err_code})")
                elif err_code == "9999": mbox.showerror("System Error", f"An unknown error occurred! (Error Code: {err_code})")
                
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


def playlist_download(link, mode, pldirectory, root):
    sync_event = threading.Event()
    stop_flag = {
        "fp": threading.Event(),
        "work": threading.Event(),
        "catch-err": threading.Event()
    }
    max_percentage = 10000

    progression = DoubleVar()
    progressText = StringVar()
    

    UI = __import__('yt_ui')
    UI.loading_progress(root, progressText, progression, max_percentage)

    def fake_progressing(exceptional_percentage):
        def body():
            print("progressing...")
            print("available:", not stop_flag["fp"].is_set())
            if not stop_flag["fp"].is_set():
                print("ok", progression.get(), exceptional_percentage)
                if(int(progression.get()) == exceptional_percentage): return
                for _ in range(int(progression.get()), exceptional_percentage):
                    print(f"{_} percent added")
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
        global p
        global videos
        global output_ext
        global err_code
        videos = []
        if not stop_flag["work"].is_set():
            try:
                def retrieve_link(): 
                    global p
                    if(re.search("playlist", link)): p = Playlist(link)
                real_progressing("Retrieving YouTube link...", 500, 2, retrieve_link)
            except Exception:
                # raiseErr("1404")
                raise Exception
                return

            if pldirectory == "": 
                raiseErr("2404")
                # raise Exception("Please provide file path!")
                return

            output_ext = None
            if mode.lower() == "video":
                output_ext = ".mp4"
            elif mode.lower() == "audio":
                output_ext = ".mp3"
            dir = folder_sorting(replace_unsupported_char(p.title), pldirectory)
            percentage_before_checking_availability = 500
            percentage_before_downloading_initiate = 2000
            global check_availability_progress
            check_availability_progress = percentage_before_checking_availability
            for i, v in enumerate(p.videos):    
                try:
                    def get_video(yt_v):
                        global videos
                        global check_availability_progress
                        check_availability(yt_v)
                        videos.append(v.streams.get_highest_resolution())
                        check_availability_progress += int(percentage_before_checking_availability / len(p.videos))
                        print(check_availability_progress)
                    real_progressing(f"Checking for the {mode.lower()}s availability... ({i+1}/{len(p.videos)})", check_availability_progress if len(p.videos) - i != 1 else percentage_before_downloading_initiate, 0, get_video, {'yt_v': v})
                except Exception:
                    raiseErr("3150")
                    return
            global downloading_video_progress
            downloading_video_progress = percentage_before_downloading_initiate   
            for i, v in enumerate(p.videos):
                try:
                    def download_video(vid, vidTitle):
                        global downloading_video_progress
                        global output_ext
                        file_dir = dir
                        vidTitle = replace_unsupported_char(vidTitle)
                        file_sorting(vid, file_dir, vidTitle, output_ext)
                        downloading_video_progress += int((max_percentage - percentage_before_downloading_initiate) / len(p.videos))
                    real_progressing(f"Downloading the {mode.lower()}... ({v.title})", downloading_video_progress if len(p.videos) - i != 1 else max_percentage, 0, download_video, {'vid': videos[i], 'vidTitle': v.title})
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
            UI.loading.destroy()
            root.attributes("-disabled", False)

        err_code = None
        mbox.showinfo("System", "Your conversion is successfully completed!")
                
        stop_flag["catch-err"].set()
        stop_flag["work"].set()
        stop_flag["fp"].set()
        return

    def catch_error():
        global err_code
        sync_event.wait()
        if not stop_flag["catch-err"].is_set():
            if err_code is not None:
                if err_code == "1404": mbox.showerror("System Error", f"Invalid YouTube Link! (Error Code: {err_code})")
                elif err_code == "2404": mbox.showerror("System Error", f"Invalid File Path! (Error Code: {err_code})")
                elif err_code == "3150": mbox.showerror("System Error", f"The video is currently unavailable, We're sorry about that! (Error Code: {err_code})")
                elif err_code == "3009": mbox.showwarning("System Warning", f"File's name doesn't support, your file has been downloaded! (Warning Code: {err_code})")
                elif err_code == "0058": mbox.showerror("System Error", f"The file is already exist! (Error Code: {err_code})")
                elif err_code == "4003": mbox.showerror("System Error", f"You don't have permission to download into this folder! (Error Code: {err_code})")
                elif err_code == "9999": mbox.showerror("System Error", f"An unknown error occurred! (Error Code: {err_code})")
                
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
