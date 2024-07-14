import random
import tkinter as tk
from PIL import ImageTk, Image

class VirtualPet:
    def __init__(self, window):
        self.window = window
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_width = 500
        self.window_height = 500

        self.treats= []

        self.img_path = 'resources/doggo.gif'
        self.img = Image.open(self.img_path)
        self.numFrames = self.img.n_frames
        self.idle = []
        for i in range(self.numFrames):
            obj = tk.PhotoImage(file = self.img_path, format = f"gif -index {i}")
            self.idle.append(obj)

        self.cycle = 0
        self.check = 1
        self.frame = self.idle[self.cycle]
        
        self.x_pos = random.randint(0, self.screen_width - self.window_width)
        self.y_pos = random.randint(0, self.screen_height - self.window_height)
        
        self.x_dir = random.randint(-4, 4)
        self.y_dir = random.randint(-4, 4)
        

        self.label = tk.Label(window, image = "")
        self.label.pack()

        self.window.overrideredirect(True)


        self.move_window()
        self.leave_treat()
        self.change_direction()
        self.update()

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

    def pause(self):
        self.x_dir = 0
        self.y_dir = 0

    def change_direction(self):
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

        self.window.after(random.randint(500, 5000), self.pause)

        # Schedule the next direction change
        self.window.after(random.randint(1000, 5000), self.change_direction)
    
    def gif_work(self):
        if self.cycle < len(self.idle) -1:
            self.cycle+=1
        else:
            self.cycle = 0

    def update(self):
            self.frame = self.idle[self.cycle]
            self.label.configure(image=self.frame)
            self.gif_work()
            self.window.attributes('-topmost', True)
            self.window.after(400, self.update)

    def leave_treat(self):
        root = tk.Toplevel()

        def close_window(event, root):
            root.destroy()    


        treat_img_path = "resources/ppixpet.png"  # Path to your treat image
        treat_image = Image.open(treat_img_path)
        treat = ImageTk.PhotoImage(treat_image)

        treat_label = tk.Label(root, image=treat)
        treat_label.image = treat
        treat_label.pack()

        treat_label.bind("<Button-1>", lambda event, win=root: win.destroy() )

        root.attributes('-topmost', True)
        root.overrideredirect(True)
        root.geometry(f"255x255+{self.x_pos}+{self.y_pos}")

        self.window.after(random.randint(5000, 15000), self.leave_treat)

    
