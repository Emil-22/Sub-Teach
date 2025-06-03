from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox, font
import subprocess
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Sub Teach\Login\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def validate_login():
    class_entry = entry_2.get()
    password_entry = entry_1.get()
    
    if class_entry == "10" and password_entry == "1234":
        window.destroy()  
        try:
            subprocess.Popen([sys.executable, "D:/Sub Teach/subjects/subjects.py"])
        except FileNotFoundError:
            messagebox.showerror("Error", "Could not find subjects.py")
    else:
        messagebox.showerror("Login Failed", "Invalid class or password")

window = Tk()

window.geometry("1920x1080")
window.configure(bg="#D9D9D9")  

try:
    custom_font = font.Font(family="Poppins", size=16)  # Increased font size to 16
except:
    # Fallback if Poppins isn't installed
    custom_font = font.Font(size=16)  # Larger fallback font

canvas = Canvas(
    window,
    bg="#D9D9D9",  # change to the grey spcified color
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)

# Background image
image_image_1 = PhotoImage(
    file=relative_to_assets("login_image_1.png"))
image_1 = canvas.create_image(
    960.0,
    540.0,
    image=image_image_1
)

# Other design elements
image_image_2 = PhotoImage(
    file=relative_to_assets("login_image_2.png"))
image_2 = canvas.create_image(
    961.0,
    539.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("login_image_3.png"))
image_3 = canvas.create_image(
    566.0,
    539.0,
    image=image_image_3
)
# Login button
button_image_1 = PhotoImage(
    file=relative_to_assets("login_button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=validate_login,
    relief="flat",
    bg="#D9D9D9",  # Changed to your specified grey color
    activebackground="#D9D9D9"  # Changed to your specified grey color
)
button_1.place(
    x=1060.0,
    y=698.0,
    width=497.0,
    height=110.0
)

# Password entry
entry_image_1 = PhotoImage(
    file=relative_to_assets("login_entry_1.png"))
entry_bg_1 = canvas.create_image(
    1309.0,
    572.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#D9D9D9",  # Changed to your specified grey color
    fg="#000716",
    highlightthickness=0,
    show="*",
    font=custom_font,  # Using the larger font
    insertbackground="#000716"  # Cursor color
)
entry_1.place(
    x=976.0,
    y=529.0,
    width=666.0,
    height=84.0
)

canvas.create_text(
    962.0,
    487.0,
    anchor="nw",
    text="Password",
    fill="#7C838A",
    font=("Poppins Medium", 25 * -1)
)

# Class entry
entry_image_2 = PhotoImage(
    file=relative_to_assets("login_entry_2.png"))
entry_bg_2 = canvas.create_image(
    1309.0,
    413.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#D9D9D9",  # Changed to your specified grey color
    fg="#000716",
    highlightthickness=0,
    font=custom_font,  # Using the larger font
    insertbackground="#000716"  # Cursor color
)
entry_2.place(
    x=976.0,
    y=370.0,
    width=666.0,
    height=84.0
)

canvas.create_text(
    962.0,
    327.0,
    anchor="nw",
    text="Class",
    fill="#7C838A",
    font=("Poppins Medium", 25 * -1)
)

# Logo or other image
image_image_4 = PhotoImage(
    file=relative_to_assets("login_image_4.png"))
image_4 = canvas.create_image(
    1309.0,
    228.0,
    image=image_image_4
)

# Make the password entry work with Enter key
entry_1.bind('<Return>', lambda event: validate_login())
# Make the class entry work with Enter key
entry_2.bind('<Return>', lambda event: validate_login())

window.resizable(False, False)
window.mainloop()