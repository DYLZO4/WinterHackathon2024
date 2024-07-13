import random
import tkinter as tk
from PIL import ImageTk, Image
import time

def pause():
    time.sleep(random.randint(500, 3000)/1000)

class VirtualPet:
    def __init__(self, window):
        self.window = window
        self.window.geometry("225x225")
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_width = 225
        self.window_height = 225
        
        self.x_pos = random.randint(0, self.screen_width - self.window_width)
        self.y_pos = random.randint(0, self.screen_height - self.window_height)
        
        self.x_dir = random.randint(-4, 4)
        self.y_dir = random.randint(-4, 4)
        
        self.window.after(10, self.move_window)
        self.window.after(random.randint(1000, 1100), self.change_direction)  

    def move_window(self):
        self.x_pos += self.x_dir
        self.y_pos += self.y_dir

        if self.x_pos <= 0 or self.x_pos >= self.screen_width - self.window_width:
            self.x_dir -= self.x_dir  
        if self.y_pos <= 0 or self.y_pos >= self.screen_height - self.window_height:
            self.y_dir -= self.y_dir

        self.window.geometry(f'+{self.x_pos}+{self.y_pos}')

        # Schedule the next move
        self.window.after(10, self.move_window)

    def change_direction(self):
        pause()
        self.x_dir = random.randint(-4, 4)
        self.y_dir = random.randint(-4, 4)

        if self.x_pos <= 0:
            self.x_dir = random.randint(-0, 4)
        if  self.x_pos >= self.screen_width - self.window_width:
            self.x_dir = random.randint(-4, 0)
        if self.y_pos <= 0:
            self.y_dir = random.randint(0, 4)
        if self.y_pos >= self.screen_height - self.window_height:
            self.y_dir = random.randint(-4, 0)

        # Schedule the next direction change
        self.window.after(random.randint(1000, 5000), self.change_direction)

if __name__ == "__main__":
    # Window to place pet
    window = tk.Tk()
    window.title("Virtual Pet")

    # Set the initial position of the window
    x_pos = 0
    y_pos = 0
    window.geometry(f'225x225+{x_pos}+{y_pos}')
    window.attributes('-topmost', True)
    window.overrideredirect(True)

    # Create virtual pet
    app = VirtualPet(window)

    # Dialogue options for pet
    dialogue = []
    img_path = 'resources/ppixpet.png'

    # Display the pet image
    img = ImageTk.PhotoImage(Image.open(img_path))
    label = tk.Label(window, image=img)
    label.pack()

    window.mainloop()

