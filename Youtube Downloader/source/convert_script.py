from pytube import *
import shutil
import tkinter.messagebox as mbox
import os
import re
import threading
# import ffmpeg
# Deal with it later (ffmpeg)


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
    asset.download(filedir, filename=result_file_name + ext)
    if not ign:
        print("Download Successful!")
        mbox.showinfo("System", "Your conversion is successfully completed!")


def one_download(link, mode, directory):
    f = None
    try:
        f = YouTube(link)
    except:
        mbox.showerror("System Error", "Invalid YouTube Link!")
        return
    if directory == "":
        mbox.showerror("System Error", "Invalid File Path!")
        return
    if mode.lower() == "video":
        check_availability(f)
        video = f.streams.get_highest_resolution()
        try:
            file_dir = directory
            f.title = replace_unsupported_char(f.title)
            file_sorting(video, file_dir, f.title, ".mp4", False)
        except WindowsError:
            print("File's name doesn't support, but it downloaded successful anyway.")
            mbox.showwarning("System Warning", "File's name doesn't support, your file has been downloaded! (Code: 3009)")
        except FileExistsError:
            print("The file is already exist!")
            mbox.showerror("System Error", "The file is already exist!")
        except PermissionError:
            print("You don't have permission to download into this folder")
            mbox.showerror("System Error", "You don't have permission to download into this folder!")
        except:
            print("An Error occurred")
            mbox.showerror("System Error", "An unknown error occurred!")

    elif mode.lower() == "audio":
        check_availability(f)
        audio = f.streams.filter(only_audio=True).first()
        try:
            afile_dir = directory
            f.title = replace_unsupported_char(f.title)
            file_sorting(audio, afile_dir, f.title, ".mp3", False)
        except WindowsError:
            print("File's name doesn't support, but it downloaded successful anyway.")
            mbox.showwarning("System Warning", "File's name doesn't support, your file has been downloaded! (Code: 3009)")
        except FileExistsError:
            print("The file is already exist!")
            mbox.showerror("System Error", "The file is already exist!")
        except PermissionError:
            print("You don't have permission to download into this folder")
            mbox.showerror("System Error", "You don't have permission to download into this folder!")
        except:
            print("An Error occurred")
            mbox.showerror("System Error", "An unknown error occurred!")


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
    if mode.lower() == "video":
        dir = folder_sorting(replace_unsupported_char(playlist.title), pldir)
        for v in playlist.videos:
            try:
                check_availability(v)
                video = v.streams.get_highest_resolution()
                v.title = replace_unsupported_char(v.title)
                file_sorting(video, dir, v.title, ".mp4", True)
            except WindowsError:
                print("File's name doesn't support, but it downloaded successful anyway.")
                mbox.showwarning("System Warning", "File's name doesn't support, your file has been downloaded! (Code: 3009)")
                shutil.rmtree(dir, ignore_errors=True)
                break
            except FileExistsError:
                print("The file is already exist!")
                mbox.showerror("System Error", "The file is already exist!")
                shutil.rmtree(dir, ignore_errors=True)
                break
            except PermissionError:
                print("You don't have permission to download into this folder")
                mbox.showerror("System Error", "You don't have permission to download into this folder!")
                shutil.rmtree(dir, ignore_errors=True)
                break
            except:
                print("An Error occurred")
                mbox.showerror("System Error", "An unknown error occurred!")
                shutil.rmtree(dir, ignore_errors=True)
                break
        print("Download Successful!")
        mbox.showinfo("System", "Your conversion is successfully completed!")
    elif mode.lower() == "audio":
        dir = folder_sorting(replace_unsupported_char(playlist.title), pldir)
        for a in playlist.videos:
            try:
                check_availability(a)
                audio = a.streams.filter(only_audio=True).first()
                a.title = replace_unsupported_char(a.title)
                file_sorting(audio, dir, a.title, ".mp3", True)
            except WindowsError:
                print("File's name doesn't support, but it downloaded successful anyway.")
                mbox.showwarning("System Warning", "File's name doesn't support, your file has been downloaded! (Code: 3009)")
                shutil.rmtree(dir, ignore_errors=True)
                break
            except FileExistsError:
                print("The file is already exist!")
                mbox.showerror("System Error", "The file is already exist!")
                shutil.rmtree(dir, ignore_errors=True)
                break
            except PermissionError:
                print("You don't have permission to download into this folder")
                mbox.showerror("System Error", "You don't have permission to download into this folder!")
                shutil.rmtree(dir, ignore_errors=True)
                break
            except:
                print("An Error occurred")
                mbox.showerror("System Error", "An unknown error occurred!")
                shutil.rmtree(dir, ignore_errors=True)
                break
        print("Download Successful!")
        mbox.showinfo("System", "Your conversion is successfully completed!")