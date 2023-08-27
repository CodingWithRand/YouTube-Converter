def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            print(i)
            return False
    return True


# print(is_prime(1111))

from tkinter import *
from tkinter import font
from tkinter import ttk
import addition_script as adds


# loading = Tk()
# progression = DoubleVar()

# loading.title("YouTube Converter")
# loading.iconbitmap("icon.ico")
# loading.resizable(FALSE, FALSE)
# loading.protocol("WM_DELETE_WINDOW", lambda: None)
# loading.geometry(adds.sizing_positioning((1000, 200), adds.win_center_pos(loading, (1000,200))))
# # root.attributes("-disabled", True)
# progressionText = Label(loading, text='Starting Task...', font=font.Font(size=20))
# progressionBar = ttk.Progressbar(loading, variable=progression, maximum=100)
# progressionText.pack()
# progressionBar.pack()

# loading.mainloop()

import tkinter as tk

app = tk.Tk()
app.title("Center Item Both Horizontally and Vertically")

# Create a label and use the grid manager to center it
label = tk.Label(app, text="Centered", font=("Helvetica", 20))
label.grid(row=0, column=0, padx=10, pady=10)

# Configure grid weights to make label expand
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

app.mainloop()


