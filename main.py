# main.py
import tkinter as tk
from tkinterdnd2 import TkinterDnD
import os

from fences import FenceManager
from icon_manager import IconManager
from layout_manager import LayoutManager


def get_desktop_path():
    desktop = os.path.expanduser("~/Desktop")
    return desktop if os.path.exists(desktop) else os.getcwd()


def main():
    # Create the root window with drag-and-drop support
    root = TkinterDnD.Tk()
    root.title("Custom Fences Organizer")
    root.geometry("800x600")
    root.withdraw()  # Hide the main window; overlays will be used

    # Load saved layout (if any)
    layout_manager = LayoutManager("config.json")
    layout_data = layout_manager.load_layout()

    # Create fence manager (creates Toplevel overlay fences)
    fence_manager = FenceManager(root, layout_data)

    # Load desktop icons (placeholder images required in assets/icons/)
    desktop_path = get_desktop_path()
    icon_manager = IconManager(root, desktop_path)
    icons = icon_manager.get_desktop_icons()

    # For now, add each icon to the first fence
    for icon in icons:
        fence_manager.add_icon_to_fence(icon)

    # Bind F2 and F12 globally to create a new fence or exit the app
    def create_new_fence(event):
        fence_manager.create_fence(100, 100)

    root.bind_all("<F2>", create_new_fence)

    def exit_app(event):
        root.quit()

    root.bind_all("<F12>", exit_app)

    root.mainloop()


if __name__ == "__main__":
    main()
