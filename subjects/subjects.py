from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
import subprocess
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Sub Teach\subjects\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def open_python_file(file_path, subject_name):
    try:
        print(f"{subject_name} button clicked! Opening {file_path} with subject: {subject_name}")
        window.destroy()
        subprocess.Popen([sys.executable, file_path, subject_name])
    except FileNotFoundError:
        messagebox.showerror("Error", f"Could not find {file_path}")

window = Tk()
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(960.0, 540.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(987.0, 539.0, image=image_image_2)

button_configs = [
    ("button_1.png", 1248.0, 669.0, "D:/Sub Teach/Main/main.py", "Nothing"),
    ("button_2.png", 775.0, 669.0, "D:/Sub Teach/Main/main.py", "Language"),
    ("button_3.png", 302.0, 669.0, "D:/Sub Teach/Main/main.py", "Math"),
    ("button_4.png", 1248.0, 518.0, "D:/Sub Teach/Main/main.py", "Nothing"),
    ("button_5.png", 775.0, 518.0, "D:/Sub Teach/Main/main.py", "SST"),
    ("button_6.png", 302.0, 518.0, "D:/Sub Teach/Main/main.py", "English"),
    ("button_7.png", 1248.0, 367.0, "D:/Sub Teach/Main/main.py", "Nothing"),
    ("button_8.png", 775.0, 367.0, "D:/Sub Teach/Main/main.py", "Science"),
    ("button_9.png", 302.0, 367.0, "D:/Sub Teach/Main/main.py", "AI")
]

buttons = []
for config in button_configs:
    img_file, x, y, target_script, subject_name = config
    button_img = PhotoImage(file=relative_to_assets(img_file))
    
    btn = Button(
        image=button_img,
        borderwidth=0,
        highlightthickness=0,
        command=lambda ts=target_script, sn=subject_name: open_python_file(ts, sn),
        relief="flat"
    )
    btn.place(x=x, y=y, width=426.0, height=110.0)
    buttons.append((btn, button_img))  # Prevent garbage collection

# Logo
image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
canvas.create_image(987.0, 227.0, image=image_image_3)

window.resizable(False, False)
window.mainloop()
