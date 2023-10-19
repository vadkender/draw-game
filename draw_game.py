
from tkinter import *
from tkinter import messagebox
from PIL import Image
import math
import re
import os

CANVAS_WIDTH = 700
CANVAS_HEIGHT = 700

commands = ["face", "move", "clear", "color", "width", "pen"]

facing = 0
pen = True
color = "black"
width = "1"

def command_list():
    helpWindow = Toplevel()
    helpWindow.geometry("500x600")
    helpWindow.config(background="light green")
    label = Label(helpWindow, font=("OCR A Extended", 20), fg="dark green", bg="light green", text="--COMMAND LIST--\n\n"
                                                                                                    "face: faces the given direction (a value in degrees, for example face 47.8)\n\n"
                                                                                                    "move: moves the given number of steps (fe. move 54)\n\n"
                                                                                                    "clear: clears the canvas\n\n"
                                                                                                    "color: changes the pen's color (supports some color names and hex values, fe. color blue)\n\n"
                                                                                                    "width: changes the thickness of the pen (fe. width 2.5)\n\n"
                                                                                                    "pen: lifts the pen up or puts it down (fe. pen up)",
                  anchor="w", justify="left", wraplength=500)
    label.pack()

def checkhex(hex):
    hex_color_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    return re.match(hex_color_pattern, hex) is not None

def clear():
    lbx, lby = canvas.coords("lb")[0], canvas.coords("lb")[1]
    canvas.delete(ALL)
    canvas.create_image(lbx, lby, image=lb, tags="lb")
    return 0

def face(clist):
    global facing
    global lb
    try:
        facing = float(clist[1])
        x, y = canvas.coords("lb")[0], canvas.coords("lb")[1]
        canvas.delete("lb")
        pil_lb = Image.open("bug.png")
        pil_lb = pil_lb.rotate(float(clist[1]))
        temp_file = "temp_image.png"
        pil_lb.save(temp_file, format="PNG")
        lb = PhotoImage(file=temp_file)
        lb = lb.subsample(5, 5)
        canvas.create_image(x, y, image=lb, tags="lb")
        os.remove(temp_file)
    except ValueError:
        messagebox.showerror(message="Error - invalid rotation angle", title="Error")

def move(clist):
    global lb
    try:
        steps = float(clist[1])
        lbx, lby = canvas.coords("lb")[0], canvas.coords("lb")[1]
        angle_rad = math.radians(facing)
        movex = steps * math.cos(angle_rad)
        movey = steps * math.sin(angle_rad)
        canvas.move("lb", movex, -movey)
        linex, liney = canvas.coords("lb")[0], canvas.coords("lb")[1]
        if pen:
            canvas.create_line(lbx, lby, linex, liney, fill=color, width=width)
    except ValueError:
        messagebox.showerror(message="Error - invalid step count", title="Error")

def pickcolor(clist):
    global color
    if clist[1] not in ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta", "gold"]:
        if checkhex(clist[1]):
            color = clist[1]
        else:
            messagebox.showerror(message="Error - invalid color name/hex value", title="Error")
    else:
        color = clist[1]

def pickwidth(clist):
    global width
    try:
        width = float(clist[1])
    except ValueError:
        messagebox.showerror(message="Error - invalid width value", title="Error")

def changepen(clist):
    global pen
    if clist[1] == "up":
        pen = False
    elif clist[1] == "down":
        pen = True
    else:
        messagebox.showerror(message="Error - invalid pen attribute", title="Error")

def draw():
    command = entry.get()
    clist = command.split()
    if len(clist) not in [1, 2]:
        messagebox.showerror(message="Error - invalid syntax", title="Error")
        return 0
    elif clist[0] not in commands:
        messagebox.showerror(message="Error - invalid syntax", title="Error")
        return 0
    elif clist[0] == "clear":
        clear()
    elif clist[0] == "face":
        face(clist)
    elif clist[0] == "move":
        move(clist)
    elif clist[0] == "color":
        pickcolor(clist)
    elif clist[0] == "width":
        pickwidth(clist)
    elif clist[0] == "pen":
        changepen(clist)

window = Tk()

window.title("Totally original drawing game")
window.config(background="light green")
canvas = Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()
lb = PhotoImage(file="bug.png")
lb = lb.subsample(5, 5)
canvas.create_image(CANVAS_WIDTH/2, CANVAS_HEIGHT/2, image=lb, tags="lb")

entry = Entry(window, font=("OCR A Extended", 20), width=32, fg="dark green")
entry.pack()

frame = Frame(window)
frame.pack()

submit_button = Button(frame, font=("OCR A Extended", 20), text="Do", command=draw, fg="dark green")
submit_button.pack(side=LEFT)

help_button = Button(frame, text="Help", command=command_list, font=("OCR A Extended", 20), fg="dark green")
help_button.pack(side="left")

window.bind("<Return>", lambda event: draw())

window.mainloop()