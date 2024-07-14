import random
import tkinter as tk
import win32gui
from PIL import ImageTk, Image

class VirtualPet:
    def __init__(self, window, selectedapplications):
        self.selectedapplications = selectedapplications
        self.window = window
        

        self.window = window
        
        self.window.wm_attributes('-transparentcolor', 'pink')
        
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.img_path = 'assets/blobert.gif'
        self.img = Image.open(self.img_path)

        self.img.convert("RGBA")
        self.window_width = self.img.width
        self.window_height = self.img.height

        
        self.cycle = 0
        self.check = 1
        self.frame = self.idle[self.cycle]
        
        self.x_pos = random.randint(0, self.screen_width - self.window_width)
        self.y_pos = random.randint(0, self.screen_height - self.window_height)
        
        self.x_dir = random.randint(-4, 4)
        self.y_dir = random.randint(-4, 4)
        

        self.label = tk.Label(window, image = "", bg= 'pink')
        self.label.pack()

        self.window.overrideredirect(True)

        self.textbox.wm_attributes('-transparentcolor', 'pink')
        self.textbox.attributes('-topmost', True)
        self.textbox.overrideredirect(True)
        self.textbox.withdraw()


        self.move_window()
        self.leave_treat()
        self.change_direction()
        self.update()

    def get_text_bubble(self):
        self.textbox_img = "assets/messagebubble.png"
        self.textbox_img = Image.open(self.textbox_img)
        self.textbox_width = self.textbox_img.width
        self.textbox_height = self.textbox_img.height
        
        self.textbox_img.convert("RGBA")
        self.textbox_img = ImageTk.PhotoImage(self.textbox_img)
        self.textbox = tk.Toplevel()
        self.textbox_label = tk.Label(self.textbox, image = self.textbox_img, bg = 'pink')
        self.textbox_label.pack() 

    def get_animation(self):
        self.numFrames = self.img.n_frames
        self.idle = []
        for i in range(self.numFrames):
            obj = tk.PhotoImage(file = self.img_path, format = f"gif -index {i}")
            self.idle.append(obj)

    def move_window(self):
        self.x_pos += self.x_dir
        self.y_pos += self.y_dir

        if self.x_pos <= 0 or self.x_pos >= self.screen_width - self.window_width:
            self.x_dir -= self.x_dir  
        if self.y_pos <= 0 or self.y_pos >= self.screen_height - self.window_height:
            self.y_dir -= self.y_dir

        self.window.geometry(f'+{self.x_pos}+{self.y_pos}')
        self.textbox.geometry(f'+{self.x_pos - int(self.textbox_width/2) - 50}+{self.y_pos-int(self.textbox_height)+70}')

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
        if(win32gui.GetForegroundWindow() not in self.selectedapplications):
            print("unproductive")
            if random.random() < 0.15:
                self.textbox.deiconify()
                get_motivation()
                self.window.after(200, self.pause)
                self.textbox.withdraw()
        else:
            print("productive")

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
        root.wm_attributes('-transparentcolor', 'pink')
        def close_window(event, root):
            root.destroy()    


        treat_img_path = "assets/petPoo.gif"  # Path to your treat image
        treat_image = Image.open(treat_img_path)
        treat = ImageTk.PhotoImage(treat_image)


        treat_label = tk.Label(root, image=treat, bg = 'pink')
        treat_label.image = treat
        treat_label.pack()

        treat_label.bind("<Button-1>", lambda event, win=root: win.destroy() )

        root.attributes('-topmost', True)
        root.overrideredirect(True)
        root.geometry(f"+{self.x_pos}+{self.y_pos}")

        self.window.after(random.randint(5000, 15000), self.leave_treat)
    

    