from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from PIL import Image, ImageTk, ImageSequence
import os
import sys
import comtypes.client
import pytesseract
import pyttsx3
import re
import time
import subprocess
from itertools import cycle

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets/frame0"
PPTS_FOLDER = OUTPUT_PATH.parent / "ppts"
SLIDES_FOLDER = OUTPUT_PATH.parent / "slides"
AVATAR_PATH = OUTPUT_PATH / "assets/avatar"

# Global state
current_slide_index = 0
slide_images = []
slide_photo = None
subject = None
is_reading = False

# Avatar animation state
avatar_talking_frames = []
avatar_silent_frame = None
avatar_current_frame = None
avatar_animation = None
is_animating = False

# TTS setup
tts_engine = pyttsx3.init()
tts_engine.setProperty('rate', 120)
tts_engine.setProperty('volume', 1.0)

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def relative_to_avatar(path: str) -> Path:
    return AVATAR_PATH / Path(path)

def load_avatar_images():
    global avatar_talking_frames, avatar_silent_frame
    
    # Load talking GIF
    talking_gif_path = relative_to_avatar("Talking.png")
    if talking_gif_path.exists():
        talking_gif = Image.open(talking_gif_path)
        avatar_talking_frames = [
            ImageTk.PhotoImage(frame.copy().resize((150, 150), Image.Resampling.LANCZOS))
            for frame in ImageSequence.Iterator(talking_gif)
        ]
    
    # Load silent frame
    silent_img_path = relative_to_avatar("silent.png")
    if silent_img_path.exists():
        silent_img = Image.open(silent_img_path).resize((150, 150), Image.Resampling.LANCZOS)
        avatar_silent_frame = ImageTk.PhotoImage(silent_img)
    
    # Create rounded rectangle background
    canvas.create_oval(1650, 50, 1850, 250, fill="#f0f0f0", outline="#333333", width=2)
    
    # Create avatar display
    canvas.avatar_display = canvas.create_image(1750, 150, image=avatar_silent_frame)

def animate_avatar():
    global avatar_animation, is_animating
    
    if not is_animating or not avatar_talking_frames:
        return
    
    try:
        next_frame = next(avatar_animation)
        canvas.itemconfig(canvas.avatar_display, image=next_frame)
        window.after(100, animate_avatar)  # Adjust timing for animation speed
    except StopIteration:
        avatar_animation = cycle(avatar_talking_frames)
        window.after(100, animate_avatar)

def convert_ppt_to_images(subject_name):
    ppt_path = PPTS_FOLDER / f"{subject_name}.pptx"
    subject_slide_folder = SLIDES_FOLDER / subject_name
    subject_slide_folder.mkdir(parents=True, exist_ok=True)

    if any(subject_slide_folder.glob("*.PNG")):
        print(f"Slides already exist for {subject_name}. Skipping conversion.")
        return

    try:
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1
        presentation = powerpoint.Presentations.Open(str(ppt_path), WithWindow=False)
        presentation.SaveAs(str(subject_slide_folder), 18)  # 18 = PNG
        presentation.Close()
        powerpoint.Quit()
        print(f"Exported slides for {subject_name}")
    except Exception as e:
        messagebox.showerror("Error", f"PowerPoint export failed: {e}")

def natural_sort_key(path_obj):
    name = path_obj.stem
    match = re.search(r'(\d+)', name)
    return int(match.group(1)) if match else 0

def load_slide_images(subject_name):
    global slide_images
    folder = SLIDES_FOLDER / subject_name
    slide_images = sorted(folder.glob("*.PNG"), key=natural_sort_key)

def clean_ocr_text(text):
    cleaned = re.sub(r'[^A-Za-z0-9.,!? \n]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def read_slide_text(index):
    global is_reading, is_animating, avatar_animation
    
    if 0 <= index < len(slide_images):
        img_path = slide_images[index]
        text = pytesseract.image_to_string(str(img_path))
        cleaned = clean_ocr_text(text)
        if cleaned:
            is_reading = True
            is_animating = True
            avatar_animation = cycle(avatar_talking_frames)
            animate_avatar()
            
            for line in cleaned.split('\n'):
                if line.strip():
                    tts_engine.say(line.strip())
                    tts_engine.runAndWait()
                    time.sleep(0.3)
            
            is_reading = False
            is_animating = False
            canvas.itemconfig(canvas.avatar_display, image=avatar_silent_frame)
        else:
            tts_engine.say("No readable text found on this slide.")
            tts_engine.runAndWait()

def show_slide(index):
    global slide_photo, current_slide_index
    current_slide_index = index
    if 0 <= index < len(slide_images):
        img = Image.open(slide_images[index])
        img = img.resize((1370, 650), Image.Resampling.LANCZOS)
        slide_photo = ImageTk.PhotoImage(img)
        canvas.create_image(302.0 + 685, 123.0 + 325, image=slide_photo)
        window.update()
        time.sleep(0.5)
        read_slide_text(index)

def next_slide():
    global current_slide_index
    if is_reading:
        return
    if current_slide_index + 1 < len(slide_images):
        current_slide_index += 1
        show_slide(current_slide_index)
    else:
        messagebox.showinfo("End", "You have reached the last slide.")

def repeat_slide():
    global current_slide_index
    if is_reading:
        return
    read_slide_text(current_slide_index)

def display_subject_ppt(subject_name):
    convert_ppt_to_images(subject_name)
    load_slide_images(subject_name)
    if slide_images:
        show_slide(0)

# Get subject from command line
if len(sys.argv) > 1:
    subject = sys.argv[1]
else:
    subject = "AI"

# GUI Setup
window = Tk()
window.geometry("1920x1080")
window.configure(bg="#FFFFFF")

canvas = Canvas(window, bg="#FFFFFF", height=1080, width=1920, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Background
bg_img1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(960.0, 540.0, image=bg_img1)

bg_img2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(988.0, 523.0, image=bg_img2)

# Buttons
btn_exit = PhotoImage(file=relative_to_assets("button_1.png"))
Button(image=btn_exit, borderwidth=0, highlightthickness=0, command=window.destroy, relief="flat").place(x=1248, y=809, width=426, height=112)

btn_next = PhotoImage(file=relative_to_assets("button_2.png"))
Button(image=btn_next, borderwidth=0, highlightthickness=0, command=next_slide, relief="flat").place(x=775, y=809, width=426, height=112)

btn_repeat = PhotoImage(file=relative_to_assets("button_3.png"))
Button(image=btn_repeat, borderwidth=0, highlightthickness=0, command=repeat_slide, relief="flat").place(x=302, y=809, width=426, height=112)

# Slide display area
canvas.create_rectangle(302.0, 123.0, 1674.0, 783.0, fill="#D9D9D9", outline="")
canvas.create_text(960, 50, text=f"Subject: {subject}", font=("Arial", 24), fill="black")

# Load and display avatar
load_avatar_images()

if subject and subject.lower() != "nothing":
    display_subject_ppt(subject)

window.resizable(False, False)
window.mainloop()