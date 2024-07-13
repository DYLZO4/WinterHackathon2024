import os
import tkinter as tk
from tkinter import ttk
import win32gui
import win32con
import time
import random 
import pyautogui
from PIL import ImageTk, Image
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

selected_applications = []
timeFocused = 0
timeUnfocused = 0

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get('OPEN_AI_KEY')
)
model = "gpt-3.5-turbo"
temperature = 1.5
max_tokens = 50
topic = ""

messages = [
    {"role": "system", "content": "You are a productivity assistant."},
    {"role": "user", "content": "give me motivation to stay focused in 10 words or less with slight aggression"}
]

def get_motivation():
    completion = client.chat.completions.create(
        model = model,
        messages= messages,
        temperature= temperature,
        max_tokens= max_tokens
    )
    return print(completion.choices[0].message.content)



class VirtualPet:
    def __init__(self, window):
        self.window = window
        #self.window.attributes('-topmost',True)
        #window.attributes("-alpha", 1)  # Set transparency level
        self.window.wm_attributes('-transparentcolor', 'pink')
        #self.window.overrideredirect(True)
        
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.img_path = 'assets/blobert.gif'
        self.img = Image.open(self.img_path)

        self.img.convert("RGBA")
        self.window_width = self.img.width
        self.window_height = self.img.height
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
        

        self.label = tk.Label(window, image = "", bg = 'pink')
        self.label.pack()

        self.window.after(10, self.move_window)
        self.window.overrideredirect(True)
        self.window.after(random.randint(1000, 1100), self.change_direction)  
        self.window.after(1, self.update)


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
        if(win32gui.GetForegroundWindow() not in selected_applications):
            print("unproductive")
            if random.random() < 0.15:
                get_motivation()
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
            self.window.after(400, self.update)


def is_alt_tab_window(hwnd):
    """Check if the window is a visible Alt-Tab window."""
    if not win32gui.IsWindowVisible(hwnd):
        return False
    if win32gui.GetParent(hwnd) != 0:
        return False
    extended_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    if extended_style & win32con.WS_EX_TOOLWINDOW != 0:
        return False
    if extended_style & win32con.WS_EX_APPWINDOW != 0:
        return True
    if win32gui.GetWindow(hwnd, win32con.GW_OWNER) == 0:
        return True
    return False

def get_visible_applications():
    """Get a list of currently visible applications in the Alt-Tab list."""
    def callback(hwnd, extra):
        if is_alt_tab_window(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                extra.append({'title': title, 'hwnd': hwnd})
    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows

# def move_window(new_root, start_x, start_y, end_x, end_y, step, interval):
#     """Move the window from start position to end position in steps."""
#     def step_move():
#         nonlocal start_x, start_y
#         if abs(start_x - end_x) < step and abs(start_y - end_y) < step:
#             start_x, start_y = end_x, end_y
#             new_root.geometry(f"+{end_x}+{end_y}")
#             new_root.after(5000, move_window_to_new_position, new_root)  # Wait 5 seconds before moving again
#         else:
#             if start_x < end_x:
#                 start_x += step
#             elif start_x > end_x:
#                 start_x -= step
#             if start_y < end_y:
#                 start_y += step
#             elif start_y > end_y:
#                 start_y -= step
#             new_root.geometry(f"+{start_x}+{start_y}")

#             if (win32gui.GetForegroundWindow() not in selected_applications):
#                 print("unproductive")
#             else:
#                 print("productive")
#             new_root.after(interval, step_move)

#     step_move()

# def move_window_to_new_position(new_root):
#     """Generate new random positions and start the movement."""
#     screen_width = new_root.winfo_screenwidth()
#     screen_height = new_root.winfo_screenheight()
#     new_x = random.randint(0, screen_width - 300)
#     new_y = random.randint(0, screen_height - 200)
#     current_pos = new_root.geometry().split("+")[1:]
#     current_x, current_y = int(current_pos[0]), int(current_pos[1])
#     move_window(new_root, current_x, current_y, new_x, new_y, step=5, interval=20)


def show_pet():
        window = tk.Tk()
        window.title=("Virtual Pet")
        
        # Set the initial position of the window
        x_pos = 0
        y_pos = 0
        window.geometry(f'+{x_pos}+{y_pos}')
        window.attributes('-topmost', True)

        # Create virtual pet
        app = VirtualPet(window)
        
        window.mainloop()

def create_checklist(apps):
    """Create a checklist of visible applications using Tkinter."""
    

    root = tk.Tk()
    root.title("Select Focus Applications")

    # Create a frame to hold the checklist
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Add a label
    ttk.Label(frame, text="Select Focus Applications:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

    # Create a dictionary to hold the IntVar() for each checkbox
    var_dict = {}
    for idx, app in enumerate(apps):
        var_dict[app['hwnd']] = tk.IntVar()
        ttk.Checkbutton(frame, text=f"{app['title']} (Handle: {app['hwnd']})", variable=var_dict[app['hwnd']]).grid(row=idx + 1, column=0, sticky=tk.W)

    # submit selection buttons 
    def print_selected():
        global selected_applications
        selected_applications = [app['hwnd'] for app in apps if var_dict[app['hwnd']].get() == 1]
        for app in selected_applications:
            print(selected_applications)
        root.destroy()
        show_pet()
        

    ttk.Button(frame, text="Submit", command=print_selected).grid(row=len(apps) + 1, column=0, pady=(10, 0))

    root.mainloop()
    
   
    

if __name__ == "__main__":
    startTime = time.time()
    endTime = time.time()
    switchTime = time.time()
    get_motivation()
    apps = get_visible_applications()
    create_checklist(apps)
    
    


# if __name__ == "__main__":
#     apps = get_visible_applications()
#     create_checklist(apps)