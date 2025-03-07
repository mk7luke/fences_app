# main.py
import tkinter as tk
from tkinter import ttk
from tkinterdnd2 import TkinterDnD
import os

from fences import FenceManager
from icon_manager import IconManager
from layout_manager import LayoutManager


def get_desktop_path():
    # Use the standard approach to get the desktop path on Windows.
    # If it doesn't exist, fall back to the current working directory.
    desktop = os.path.expanduser("~/Desktop")
    if os.path.exists(desktop):
        return desktop
    else:
        return os.getcwd()


def main():
    # Create the main window with drag-and-drop support
    root = TkinterDnD.Tk()
    root.title("Custom Fences Organizer")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")

    # Initialize the layout manager and load saved layout (if any)
    layout_manager = LayoutManager("config.json")
    layout_data = layout_manager.load_layout()

    # Create the fence manager (this creates one or more fences based on layout data)
    fence_manager = FenceManager(root, layout_data)

    # Initialize the icon manager using the user's desktop path
    desktop_path = get_desktop_path()
    icon_manager = IconManager(root, desktop_path)
    icons = icon_manager.get_desktop_icons()

    # Add each desktop icon to the first fence (or assign based on layout if available)
    for icon in icons:
        fence_manager.add_icon_to_fence(icon)

    # Create a "Save Layout" button to store the current layout configuration
    def save_layout():
        layout = fence_manager.get_layout()
        layout_manager.save_layout(layout)
        print("Layout saved.")

    save_button = ttk.Button(root, text="Save Layout", command=save_layout)
    save_button.pack(side="bottom", pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
