import tkinter as tk
from tkinter import ttk
import win32gui
import win32con

selected_applications = []

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
        

    ttk.Button(frame, text="Submit", command=print_selected).grid(row=len(apps) + 1, column=0, pady=(10, 0))

    root.mainloop()
    


if __name__ == "__main__":
    apps = get_visible_applications()
    create_checklist(apps)
