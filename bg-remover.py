import requests
import easygui
from time import sleep
from PIL import Image

print("Welcome to an Artificial Image Background remover program!\n")

print("This program is made in python. By import the API from \"remove.bg\" \n"
      "There are two background remover engine to use in the program\n"
      "You can decide to use the remove.bg API or Pillow python package\n")

print("The remove.bg API is an Artificial API that has been trained enough to select the main object, and can remove"
      " its background image. \nThis engine is good for images that have multiple color as a background.\n")

print("The Pillow python package is the built-in python package. It can only remove single color background image.")
print("You must put the color of the background image in RGB format. So, I hope you know it! (Layout: R,G,B such as 255,0,0)\n")

print("(btw, pls consider use the pillow package. if you use the remove.bg, i have to pay for it TT)\n")
print("Special Thank to ChatGPT for some of the code (Go use it, it is a very good tool)\n")

print("Here are the commands to use this program.\n")

print("Option Commands\n"
      "rbg - Use the remove.bg API\n"
      "pilw - Use the pillow python package\n")

print("CV option commands\n"
      "dir - Upload image from your computer\n"
      "url - Upload image from web url\n")

print("Exit command: exit\n")

print("DONT FORGET TO GIVE THE FILE EXTENSION! OR ELSE YOU'LL GET THE CORRUPTED FILE OR IT WILL CAUSE ERROR!")

dbg = True

while True:

    sys_opt = input()
    if sys_opt == "rbg":
        sleep(0.5)
        print("Engine Selected - remove.bg API")
        up_meth = input()
        if up_meth == "dir":
            sleep(0.5)
            print("Upload Method Selected - from computer")
            sleep(1)
            print("Selecting image file...")
            input_path = easygui.fileopenbox(title="Select image file")
            sleep(0.5)
            print("Selecting new image directory...")
            output_path = easygui.filesavebox(title="Save file to...")
            sleep(0.5)
            print("Image directory selected: At %s" % output_path)

            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                files={'image_file': open(input_path, 'rb')},
                data={'size': 'auto'},
                headers={'X-Api-Key': 'HXdCdqFSDFzkU4JeXVRUvETT'},
            )
            if response.status_code == requests.codes.ok:
                with open(output_path, 'wb') as out:
                    out.write(response.content)
                print("Download completed!")
            else:
                print("Error:", response.status_code, response.text)

        elif up_meth == "url":
            sleep(0.5)
            print("Upload Method Selected - from web url")
            sleep(1)
            _url = input("Image link here: ")
            sleep(0.5)
            print("Selecting new image directory...")
            output_path = easygui.filesavebox(title="Save file to...")
            sleep(0.5)
            print("Image directory selected: At %s" % output_path)

            response = requests.post(
                'https://api.remove.bg/v1.0/removebg',
                data={
                    'image_url': _url,
                    'size': 'auto'
                },
                headers={'X-Api-Key': 'HXdCdqFSDFzkU4JeXVRUvETT'},
            )
            if response.status_code == requests.codes.ok:
                with open('no-bg.png', 'wb') as out:
                    out.write(response.content)
                print("Download completed!")
            else:
                print("Error:", response.status_code, response.text)

    elif sys_opt == "pilw":
        sleep(0.5)
        print("Engine Selected - Pillow Package")
        sleep(1)
        print("Selecting image file...")
        input_path = easygui.fileopenbox(title="Select image file")
        sleep(0.5)
        print("Selecting new image directory...")
        output_path = easygui.filesavebox(title="Save file to...")
        sleep(0.5)
        print("Image directory selected: At %s" % output_path)

        Color3 = input("Image's Background Color: ")

        try:
            orgimg = Image.open(input_path)
            orgimg = orgimg.convert("RGBA")
            imgdatas = orgimg.getdata()

            newData = []
            for item in imgdatas:
                rgb = Color3.split(",")
                if item[0] == int(rgb[0]) and item[1] == int(rgb[1]) and item[2] == int(rgb[2]):
                    newData.append((int(rgb[0]), int(rgb[1]), int(rgb[2]), 0))
                else:
                    newData.append(item)

            orgimg.putdata(newData)

            orgimg.save(output_path, "PNG")
            print("Download completed!")
        except:
            print("An error occurred.")

    elif sys_opt == "exit":
        exit()

    else:
        if dbg == True:
            dbg = False
            print()
        else:
            print("Invalid Command")
