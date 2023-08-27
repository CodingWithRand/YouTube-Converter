import pkg_resources
import subprocess
import types
from lxml import etree

# Check and automatically install unavailable package.

def get_available_packages():
    available_packages = list()
    installed_packages = pkg_resources.working_set
    for package in installed_packages:
        available_packages.append(package.key)
    return available_packages

def checking_package(package_name):
    packages = get_available_packages()
    for package in packages:
        if package == package_name:
            return True
    return False

def install_package(package_name):
    try:
        subprocess.check_call(['pip', 'install', package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}: {str(e)}")

from tkinter import *
from tkinter import font


def win_center_pos(window, win_size):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    pos = (int((screen_width/2) - (win_size[0]/2)), int((screen_height/2) - (win_size[1]/2)))
    return pos


def sizing_positioning(size, pos):
    return f"{size[0]}x{size[1]}+{pos[0]}+{pos[1]}"


def show_all_font_styles():
    # Create an instance of tkinter frame
    win = Tk()
    win.geometry("750x350")
    win.title('Font List')
    # Create a list of font using the font-family constructor
    fonts = list(font.families())
    fonts.sort()

    def fill_frame(frame):
        for f in fonts:
            # Create a label to display the font
            label = Label(frame, text=f, font=(f, 14)).pack()

    def onFrameConfigure(canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Create a canvas
    canvas = Canvas(win, bd=1, background="white")
    # Create a frame inside the canvas
    frame = Frame(canvas, background="white")
    # Add a scrollbar
    scroll_y = Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side="right", fill="y")
    canvas.pack(side="left", expand=1, fill="both")
    canvas.create_window((5, 4), window=frame, anchor="n")
    frame.bind("<Configure>", lambda e, canvas=canvas: onFrameConfigure(canvas))
    fill_frame(frame)
    win.mainloop()


def parsing_XML(xml):
    try:
        parsed_xml = etree.fromstring(xml)
        return parsed_xml
    except Exception as e:
        raise Exception("Incorrect XML syntax found: ", str(e))
    

def update_component_dict(old_dict, objTag, obj, tkobj):
    old_dict.update({objTag:
    {
        "Parent": obj.getparent().tag,
        "Object": tkobj
    }})


def rgb(red, green, blue):
    return "#{:02x}{:02x}{:02x}".format(red, green, blue)