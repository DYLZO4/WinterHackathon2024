import random
import tkinter as tk
import pyautogui
from PIL import ImageTk, Image

def moveLateral():
    print("G")
    global x_pos, x_dir

    # Update position
    x_pos += x_dir

    # Check if the window hits the edge of the screen
    if x_pos <= 0 or x_pos >= screen_width - window_width:
        x_pos -= x_dir

    # Move the window
    window.geometry(f'+{x_pos}+{y_pos}')

    # Repeat after a short delay
    window.after(10, moveLateral)

def moveVertical():
    print("Z")
    global y_pos, y_dir
    y_pos += y_dir

    if y_pos >= 0 or y_pos <= screen_height - window_height:
       y_pos -= y_dir

    # Move the window
    window.geometry(f'+{x_pos}+{y_pos}')

    # Repeat after a short delay
    window.after(10, moveVertical)

#Window to place pet
window = tk.Tk()
window.title=("Virtual Pet")
x= 500

def eventHandler():
    cycle = random.choice([0, 4])

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_pos = 0
y_pos = 0
x_dir = 2
y_dir = 2

# Set the dimensions of the window
window_width = 225
window_height = 225
window.attributes('-topmost',True)
window.overrideredirect(True)

# Set the initial position of the window
window.geometry(f'{window_width}x{window_height}+{x_pos}+{y_pos}')

#Handle Events

#Dialogue options for pet
dialogue = []
img = 'resources/ppixpet.png'


# #
# window.config(highlightbackground='black')
# window.overrideredirect(True)
# window.wm_attributes('-transparentcolor','black')

#Make the pet movable
img = ImageTk.PhotoImage(Image.open(img))

label = tk.Label(window,image = img)
label.pack()



window.mainloop()
  
def animate(cycle, frames, eventNum, firstNum, lastNum):
    if cycle < len(frames) - 1:
        cycle+=1
    else:
        cycle = 0
        eventNum = random.randrange(firstNum, lastNum+1)
    return cycle, eventNum



    




