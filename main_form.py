from pathlib import Path
import subprocess
import time

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Learn DUT\Year 3\PBL5\Interface\sign-recognition-app\assets\mainframe")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("800x600")
window.configure(bg = "#FFFFFF")

def close_form():
    subprocess.Popen(["python", "recognition_form.py", "--opt", "0"])
    time.sleep(1)
    window.destroy()
    
def close_form_for_stream():
    subprocess.Popen(["python", "recognition_form.py", "--opt", "1"])
    time.sleep(1)
    window.destroy()

def end_form():
    window.destroy()

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 800,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    800.0,
    67.0,
    fill="#2D80FC",
    outline="")

canvas.create_text(
    158.0,
    14.0,
    anchor="nw",
    text="SIGN LANGUAGE RECOGNIZER",
    fill="#000000",
    font=("Inter Bold", 32 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=close_form,
    relief="flat"
)
button_1.place(
    x=67.0,
    y=93.0,
    width=172.0,
    height=44.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=close_form_for_stream,
    relief="flat"
)
button_2.place(
    x=314.0,
    y=93.0,
    width=172.0,
    height=44.0
)

image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    400.0,
    395.0,
    image=image_image_1
)

button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=end_form,
    relief="flat"
)
button_3.place(
    x=561.0,
    y=93.0,
    width=172.0,
    height=44.0
)
window.resizable(False, False)
window.mainloop()
