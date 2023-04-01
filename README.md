# bg-remover-GUI
A Tkinter GUI for BackgroundRemover

![Alt Text](https://github.com/Steve-Shambles/bg-remover-GUI/blob/main/screenshot00_bgrv1.png)


BG Remover GUI V1.0

By Steve Shambles (c) April 2023
Source code is under MIT Licence.
This program is Freeware.

BG Remover GUI is a simple interface for the
excellent BackgroundRemover library By Nadermx at GitHub:
https://github.com/nadermx/backgroundremover


Python requirements to run the code:

Pip3 install torch
pip3 install backgroundremover
pip3 install Pillow
pip3 install ffmpeg-python

Instructions:

1. Click "Load image" button and choose an image using the file selector.

2. Choose an A.I model from the drop-down combobox, select "Standard" 
   if you not sure, "Human" if it is a person in the image, or "matte"
   if both these do not work well. Generally speaking try all 3 
   to find the best result. 

3. Now click "Process Image", note the "Please Wait...." 
   in the right panel, most images resolve in 30 seconds or less
   depending on your machine\memory.

4. If you are happy with the new image you can click the "Save Image" 
   button. This will save the image with a unique name using, 
   the name of the A.I model you used joined with a timestamp, eg. 
   "Human_01-Apr-2023-09.53-23s.png"
   The processed image is saved as a transparent PNG file.
   
5. You can click on the  "View Saved Images" button any time and 
   your system file browser should pop up and display your saved images
   allowing you to copy, delete or view them as you wish.

I wrote this program on a Windows 7 PC using Python V3.67,
but I see no reason why it should not work on any Windows or
Linux machine, though they remain untested.

As for creating an executable, Pyinstaller works and the exe runs fine
on my machine but I think there may be a model missing type
problem on a machine that doesnt have Pytorch installed.
I tried to isolate the 3 models i'm using but i can't at this time
work it out and I'm not sure where to place the files anyway.
If I do resolve this I will update the program.


To make your own executable:
pip3 pyinstaller
then: 

pyinstaller  bgr_V1.py -n bgr --windowed --onefile

change "bgr_V1.py" to wahatever the source file you 
are using is named if different of course.


Steve Shambles.
