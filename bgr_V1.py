""" Bg Remover V1. By Steve Shambles April 2023.
    Removes the background from most images using A.I.
"""
from datetime import datetime
import os
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, Menu
import shutil
import subprocess
import sys
import webbrowser as web

from PIL import Image, ImageTk

# I dont actually think this is needed?
import backgroundremover


root = tk.Tk()
root.title('Bg Remover V1. By Steve Shambles 2023')
root.resizable(False, False)


class Fs():
    """ Global variables, its wrong, but its the way I do it. """
    file_name = ''
    thumb_size = 400, 400
    combo_models = ['Standard', 'Human', 'Matte']
    current_model = 'Standard'


def save_image():
    """ Save processed image to saved_images folder in prg root. """
    old_file_name = 'output.png'
    dest_folder = 'saved_images'
    # current_dir = os.getcwd()
    time_stamp = datetime.now().strftime('%d-%b-%Y-%H.%M-%Ss')
    new_file_name = f'{Fs.current_model}_{time_stamp}.png'
    file_path = os.path.join(dest_folder, new_file_name)

    shutil.copy(old_file_name, dest_folder)
    os.rename(os.path.join(dest_folder, old_file_name), file_path)

    try:
        os.remove(old_file_name)
    except:
        pass

    messagebox.showinfo('Processed Image Saved',
                        'Image saved to "saved_images" folder')
    save_btn.configure(state="disabled")


def clear_old_img():
    """ Clear out old processed image and replace with a background. """
    bg_image = Image.open(r'data/background.png')
    bg_photo = ImageTk.PhotoImage(bg_image)
    processed_lab.configure(image=bg_photo)
    processed_lab.image = bg_photo


def process_image():
    """ This is where we call the exe to do all the dirty work. """
    if Fs.current_model == '':
        return
    if Fs.current_model == 'Standard':
        run_it = r'backgroundremover -i ' + '"' + str(Fs.file_name) + '"' + ' -o ' + '"output.png"'

    if Fs.current_model == 'Human':
        run_it = r'backgroundremover -i ' + '"' + str(Fs.file_name) + '"' + ' -m "u2net_human_seg" -o ' + '"output.png"'

    if Fs.current_model == 'Matte':
        run_it = r'backgroundremover -i ' + '"' + str(Fs.file_name) + '"' + ' -ae 15 -o ' + '"output.png"'

    processed_lab.configure(image=None)

    clear_old_img()

    save_btn.configure(state="disabled")
    load_img_btn.configure(state="disabled")
    process_button.configure(state="disabled")
    model_combo.configure(state="disabled")
    processed_frame.config(text='Please wait....')
    processed_frame.update()

    try:
        subprocess.run(run_it, shell=True)

        processed_frame.config(text=str(Fs.current_model) + ' model')
        new_image = Image.open('output.png')
        new_image.thumbnail(Fs.thumb_size)
        processed_image = ImageTk.PhotoImage(new_image)
        processed_lab.configure(image=processed_image)
        processed_lab.image = processed_image
        save_btn.configure(state="normal")
        process_button.configure(state="normal")
        load_img_btn.configure(state="normal")
        model_combo.configure(state="normal")

    except:
        messagebox.showinfo('BG Remover Program Information',
                            'There was an error\n'
                            'Possible model files missing\n'
                            'or not finished downloading\n'
                            'in the background yet\n\n'
                            'Please try again in a few minutes.')


def start_process_image_thread():
    """ This starts thread so GUI does no freeze up. """
    thread = threading.Thread(target=process_image)
    thread.start()


def load_placeholders():
    """ Load in a shaded bg image as placeholders. """
    image = Image.open(r'data/background.png')
    image.thumbnail(Fs.thumb_size)
    original_image = ImageTk.PhotoImage(image)
    original_lab.configure(image=original_image)
    original_lab.image = original_image
    # Display the  image in the right panel
    processed_image = ImageTk.PhotoImage(image)
    processed_lab.configure(image=original_image)
    processed_lab.image = original_image


def load_image():
    " Give user file requestor to choose an image. """
    Fs.file_name = tk.filedialog.askopenfilename()
    if Fs.file_name:
        # Load the image using Pillow
        image = Image.open(Fs.file_name)
    else:
        # The user didn't select an image
        return

    image.thumbnail(Fs.thumb_size)
    # Display the original image in the left panel
    original_image = ImageTk.PhotoImage(image)
    original_lab.configure(image=original_image)
    original_lab.image = original_image

    # Resize the processed image frame to match the size of the loaded image
    processed_lab.config(width=image.width, height=image.height)

    bg_image = Image.open(r'data/background.png')
    bg_image = bg_image.resize((image.width, image.height), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    processed_lab.configure(image=bg_photo)
    processed_lab.image = bg_photo
    process_button.configure(state="normal")


def open_save_images_folder():
    """File browser to view contents of program folder."""
    web.open('saved_images')


def model_combo_event(event):
    """ Catch user changing model in combobox. """
    Fs.current_model = event.widget.get()


def help_text():
    """Show help text file."""
    web.open(r'data\bgr_help.txt')


def about_menu():
    """About program msgbox."""
    messagebox.showinfo('BG Remover Program Information',
                        'BG Remover V1\n\n'
                        'Freeware by Steve Shambles\n'
                        'Source code MIT Licence.\n'
                        'See help file for more details.\n\n'
                        '(c) April 2023\n')


def donate_me():
    """User splashes the cash here!"""
    web.open('https:\\paypal.me/photocolourizer')


def visit_github():
    """View source code and my other Python projects at GitHub."""
    web.open('https://github.com/Steve-Shambles?tab=repositories')


def exit_bgr():
    """Yes-no requestor to exit program."""
    ask_yn = messagebox.askyesno('Question',
                                 'Quit BG Remover?')
    if ask_yn is False:
        return
    root.destroy()
    sys.exit()


# check background image and help text available.
err = False
if not os.path.isfile(r'data/background.png'):
    err = True
if not os.path.isfile(r'data/bgr_help.txt'):
    err = True

if err:
    messagebox.showinfo('File missing error',
                        'background.png or bgr_help.txt\n'
                        'is missing from data folder\n'
                        'please fix or re-install.')
    root.destroy()
    sys.exit()


# check folder exists or create if not.
if not os.path.exists('saved_images'):
    os.makedirs('saved_images')


# Create the left panel for the original image
original_frame = tk.LabelFrame(root, text='Original Image',
                               width=350, height=350)
original_frame.grid(padx=10, pady=10, row=0, column=0)
original_lab = tk.Label(original_frame)
original_lab.grid()

# Create the right panel for the processed image
processed_frame = tk.LabelFrame(root, text='Processed Image',
                                width=350, height=350)
processed_frame.grid(padx=10, pady=10, row=0, column=1)
processed_lab = tk.Label(processed_frame)
processed_lab.grid()


btns_frame = tk.LabelFrame(root)
# Create the button to select an image
load_img_btn = tk.Button(btns_frame, text="Load Image",
                         command=load_image)
load_img_btn.grid(row=0, column=0, padx=8, pady=8)


# model combo
model_combo = ttk.Combobox(btns_frame, width=10,
                           values=Fs.combo_models)
model_combo.grid(row=0, column=1, padx=8)
model_combo.configure(state="readonly")
model_combo.current(0)


# Create the button to process the image
process_button = tk.Button(btns_frame, text="Process Image",
                           command=start_process_image_thread,
                           state="disabled")
process_button.grid(row=0, column=2, padx=8)


# button to save image
save_btn = tk.Button(btns_frame, text="Save Image",
                     command=save_image, state="disabled")
save_btn.grid(row=0, column=3, padx=8)
btns_frame.grid()

# btn to open saved_images folder
saved_images_btn = tk.Button(btns_frame, text="View Saved Images",
                             command=open_save_images_folder)
saved_images_btn.grid(row=0, column=4, padx=8)
btns_frame.grid(pady=16, columnspan=20)

load_placeholders()

# File menu
# Pre-load icons for drop-down menu.
try:
    help_icon = ImageTk.PhotoImage(file=r'data/icons/help-16x16.ico')
    about_icon = ImageTk.PhotoImage(file=r'data/icons/about-16x16.ico')
    exit_icon = ImageTk.PhotoImage(file=r'data/icons/exit-16x16.ico')
    donation_icon = ImageTk.PhotoImage(file=r'data/icons/donation-16x16.ico')
    github_icon = ImageTk.PhotoImage(file=r'data/icons/github-16x16.ico')
except:
    messagebox.showinfo('BG Remover Program Information',
                        'There was an error\n'
                        'Icons are missing from the data folder\n'
                        'Please fix or re-install')
    root.destroy()
    sys.exit()


menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)

file_menu.add_command(label='Help', compound='left',
                      image=help_icon, command=help_text)
file_menu.add_command(label='About', compound='left',
                      image=about_icon, command=about_menu)
file_menu.add_separator()
file_menu.add_command(label='Python source code on GitHub', compound='left',
                      image=github_icon, command=visit_github)
file_menu.add_command(label='Make a small donation via PayPal',
                      compound='left',
                      image=donation_icon, command=donate_me)
file_menu.add_separator()
file_menu.add_command(label='Exit', compound='left',
                      image=exit_icon, command=exit_bgr)
root.config(menu=menu_bar)


model_combo.bind("<<ComboboxSelected>>", model_combo_event)

root.eval('tk::PlaceWindow . Center')
root.protocol('WM_DELETE_WINDOW', exit_bgr)


root.mainloop()
