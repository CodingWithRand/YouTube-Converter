from pytubefix import *
# from moviepy.editor import *
from tkinter import *
from time import sleep
from tkinter import messagebox as mbox
from addition_script import get_ffmpeg_path
import tempfile
import os
import subprocess
import re
import traceback
import threading

"""
After update your pytubefix package, please add the following code to innertube.py in pytubefix package:

import sys
import webbrowser
from tkinter import messagebox

def ui_oauth_verifier(verification_url: str, user_code: str):
    webbrowser.open(verification_url)
    messagebox.showinfo("OAuth Verification", f"OAuth portal has been opened in your default browser. Please enter the code: {user_code} and complete the verification process before clicking \"OK\" button. ")

And replace _default_oauth_verifier function with the following code:

def _default_oauth_verifier(verification_url: str, user_code: str):
    if(sys.stdin is not None):
        print(f'Please open {verification_url} and input code {user_code}')
        input('Press enter when you have completed this step.')
    else:
        ui_oauth_verifier(verification_url, user_code)
    
"""

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


def file_sorting(filedir, file_name):
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
    return result_file_name


def one_download(link, mode, res, directory, root):
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
        global audio
        global err_code
        if not stop_flag["work"].is_set():
            try:
                def retrieve_link(): 
                    global f
                    f = YouTube(link, use_oauth=True, allow_oauth_cache=True)
                real_progressing("Retrieving YouTube link...", 100, 2, retrieve_link)
            except Exception:
                raiseErr("1404")
                # raise Exception
                return

            if directory == "": 
                raiseErr("2404")
                # raise Exception("Please provide file path!")
                return
            
            try:
                def get_video(yt_v, mode):
                    global video
                    global audio
                    check_availability(yt_v)
                    video = None
                    if mode == "video": video = f.streams.filter(res=res, progressive=False, file_extension="mp4").first()
                    audio = f.streams.filter(only_audio=True, file_extension="mp4").first()
                    if (mode == "video" and video is None) or audio is None:
                        raise Exception("3404")
                real_progressing(f"Checking for the {mode.lower()} availability...", 200, 2, get_video, {'yt_v': f, 'mode': mode.lower()})
            except Exception as e:
                if str(e) == "3404": raiseErr("3404")
                else:
                    traceback_str = traceback.format_exc()
                    raiseErr("9999")
                    mbox.showerror("System Error", f"{traceback_str}")
                    # raise e
                    return

            try:
                def download(title, audio, video=None):
                    file_dir = directory
                    title = replace_unsupported_char(title)
                    title = file_sorting(file_dir, title)
                    if video is not None:
                        vp = video.download(output_path=tempfile.gettempdir(), filename_prefix=title)
                        ap = audio.download(output_path=tempfile.gettempdir(), filename_prefix=title)
                        subprocess.run([get_ffmpeg_path(), '-i', vp, '-i', ap, '-c', 'copy', f'{file_dir}/{title}.mp4'])
                        os.remove(vp)
                        os.remove(ap)
                    else:
                        audio.download(output_path=file_dir, filename_prefix=title)
                if mode.lower() == "video" and video is not None:
                    real_progressing("Downloading the video...", 1000, 1, download, {'title': f.title, 'audio': audio, 'video': video})
                elif mode.lower() == "audio":
                    real_progressing("Downloading the audio...", 1000, 1, download, {'title': f.title, 'audio': audio})
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
                elif err_code == "3404": mbox.showerror("System Error", f"The video resolution is not available! (Error Code: {err_code})")
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


def playlist_download(link, mode, res, pldirectory, root):
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
        global audios
        global err_code
        audios = []
        videos = []
        if not stop_flag["work"].is_set():
            try:
                def retrieve_link(): 
                    global p
                    if(re.search("playlist", link)): p = Playlist(link, use_oauth=True, allow_oauth_cache=True)
                real_progressing("Retrieving YouTube link...", 500, 2, retrieve_link)
            except Exception:
                # raiseErr("1404")
                raise Exception
                return

            if pldirectory == "": 
                raiseErr("2404")
                # raise Exception("Please provide file path!")
                return
            
            dir = folder_sorting(replace_unsupported_char(p.title), pldirectory)
            percentage_before_checking_availability = 500
            percentage_before_downloading_initiate = 2000
            global check_availability_progress
            check_availability_progress = percentage_before_checking_availability
            global warning_shown
            warning_shown = False
            for i, v in enumerate(p.videos):    
                try:
                    def get_video(yt_v, mode):
                        global audios
                        global warning_shown
                        global videos
                        global check_availability_progress
                        res_table = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]
                        check_availability(yt_v)
                        video = None
                        if mode == "video": video = v.streams.filter(res=res, progressive=False, file_extension="mp4").first()
                        audio = v.streams.filter(only_audio=True, file_extension="mp4").first()
                        if mode == "video" and video is None:
                            res_table = res_table[:res_table.index(res) + 1][::-1]
                            for resolution in res_table:
                                video = v.streams.filter(res=resolution, progressive=False, file_extension="mp4").first()
                                if video is not None and not warning_shown:
                                    mbox.showwarning("System Warning", f"A video in the playlist in the specified resolution is not available, will proceed to migrate it to the available resolution. This process will be applied to other videos as well! (Warning Code: 2066)")
                                    if not warning_shown: warning_shown = True
                                    break
                        if (mode == "video" and video is None) or audio is None:
                            raise Exception("3404")
                        if mode == "video": videos.append(video)
                        audios.append(audio)
                        check_availability_progress += int(percentage_before_checking_availability / len(p.videos))
                        print(check_availability_progress)
                    real_progressing(f"Checking for the {mode.lower()}s availability... ({i+1}/{len(p.videos)})", check_availability_progress if len(p.videos) - i != 1 else percentage_before_downloading_initiate, 0, get_video, {'yt_v': v, 'mode': mode.lower()})
                except Exception as e:
                    if str(e) == "3404": raiseErr("3404")
                    else:
                        traceback_str = traceback.format_exc()
                        raiseErr("9999")
                        mbox.showerror("System Error", f"{traceback_str}")
                        # raise e
                        return
            global downloading_video_progress
            downloading_video_progress = percentage_before_downloading_initiate   
            for i, v in enumerate(p.videos):
                try:
                    def download(title, audio, video=None):
                        global downloading_video_progress
                        file_dir = dir
                        title = replace_unsupported_char(title)
                        title = file_sorting(file_dir, title)
                        if video is not None:
                            vp = video.download(output_path=tempfile.gettempdir(), filename_prefix=title)
                            ap = audio.download(output_path=tempfile.gettempdir(), filename_prefix=title)
                            subprocess.run([get_ffmpeg_path(), '-i', vp, '-i', ap, '-c', 'copy', f'{file_dir}/{title}.mp4'])
                            os.remove(vp)
                            os.remove(ap)
                        else:
                            audio.download(output_path=file_dir, filename_prefix=title)
                        downloading_video_progress += int((max_percentage - percentage_before_downloading_initiate) / len(p.videos))
                    if mode.lower() == "video":
                        real_progressing(f"Downloading the video... ({v.title})", downloading_video_progress if len(p.videos) - i != 1 else max_percentage, 0, download, {'title': v.title, 'audio': audios[i], 'video': videos[i]})
                    elif mode.lower() == "audio":
                        real_progressing(f"Downloading the audio... ({v.title})", downloading_video_progress if len(p.videos) - i != 1 else max_percentage, 0, download, {'title': v.title, 'audio': audios[i]})
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
                elif err_code == "2066": mbox.showwarning("System Warning", f"A video in the playlist in the specified resolution is not available, successfully migrated to the available resolution! (Warning Code: {err_code})")
                elif err_code == "3150": mbox.showerror("System Error", f"The video is currently unavailable, We're sorry about that! (Error Code: {err_code})")
                elif err_code == "3404": mbox.showerror("System Error", f"The video resolution is not available! (Error Code: {err_code})")
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
