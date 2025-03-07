# icon_manager.py
import os
import tkinter as tk
from PIL import Image, ImageTk


class IconWidget(tk.Label):
    def __init__(self, master, icon_path, icon_image, **kwargs):
        super().__init__(master, image=icon_image, **kwargs)
        self.icon_path = icon_path
        self.image = icon_image  # Keep a reference to avoid garbage collection
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self._drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.lift()

    def do_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.place(x=new_x, y=new_y)

    def stop_drag(self, event):
        self._drag_data = {"x": 0, "y": 0}


class IconManager:
    def __init__(self, master, desktop_path):
        self.master = master
        self.desktop_path = desktop_path
        self.icon_size = (64, 64)  # Desired icon size

    def get_desktop_icons(self):
        icons = []
        if not os.path.exists(self.desktop_path):
            return icons

        # Scan the desktop folder for shortcut files (.lnk or .url)
        for file in os.listdir(self.desktop_path):
            if file.lower().endswith(".lnk") or file.lower().endswith(".url"):
                full_path = os.path.join(self.desktop_path, file)
                icon_image = self.get_icon_image(full_path)
                if icon_image:
                    # Create a draggable icon widget
                    widget = IconWidget(self.master, full_path, icon_image)
                    # Initially place the icon at a default position; later it can be moved into a fence
                    widget.place(x=100, y=100)
                    icons.append(widget)
        return icons

    def get_icon_image(self, icon_path):
        # For simplicity, load a placeholder image from assets.
        # A more advanced implementation would extract the actual icon from the shortcut.
        try:
            image = Image.open("assets/icons/placeholder.png")
            image = image.resize(self.icon_size, Image.ANTIALIAS)
            icon_image = ImageTk.PhotoImage(image)
            return icon_image
        except Exception as e:
            print("Error loading icon image:", e)
            return None
