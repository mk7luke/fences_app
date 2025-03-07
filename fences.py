# fences.py
import tkinter as tk

# Define a "magic" transparent color; adjust if needed.
MAGIC_COLOR = "magenta"


class Fence(tk.Toplevel):
    def __init__(
        self,
        master,
        fence_id,
        x,
        y,
        width=300,
        height=200,
        bg_color=MAGIC_COLOR,
        border_color="red",
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        self.fence_id = fence_id
        self.overrideredirect(True)  # Remove title bar and borders
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.config(bg=bg_color)
        # Make the bg_color fully transparent so the wallpaper shows through
        self.attributes("-transparentcolor", bg_color)
        # We keep the window fully opaque (alpha=1.0) so that drawn elements (like the border) appear normally.
        self.attributes("-alpha", 1.0)
        self.icons = []  # To hold any icon widgets placed inside this fence

        # Create a Canvas that fills the Toplevel.
        # The Canvas background is set to the same transparent color.
        self.canvas = tk.Canvas(
            self, width=width, height=height, bg=bg_color, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        # Draw a rectangle border that will be visible (since its outline is not the magic color)
        self.canvas.create_rectangle(
            0, 0, width - 1, height - 1, outline=border_color, width=2
        )

        # Bind mouse events on the canvas to enable dragging the fence window.
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.do_drag)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drag)
        # Also bind on the Toplevel in case you click on a non-canvas area.
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self._drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        # Record the starting point for dragging.
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_drag(self, event):
        # Calculate the new position and update the window location.
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.geometry(f"+{new_x}+{new_y}")

    def stop_drag(self, event):
        self._drag_data = {"x": 0, "y": 0}

    def add_icon(self, icon_widget, x=None, y=None):
        # Place an icon widget inside the fence's canvas.
        icon_widget.master = self
        self.icons.append(icon_widget)
        if x is None:
            x = 10
        if y is None:
            y = 10
        icon_widget.place(in_=self.canvas, x=x, y=y)


class FenceManager:
    def __init__(self, master, layout_data=None):
        self.master = master
        self.fences = {}
        self.next_fence_id = 1
        if layout_data and "fences" in layout_data:
            for fence_data in layout_data["fences"]:
                self.create_fence_from_data(fence_data)
        else:
            # Create a default fence if no layout exists.
            self.create_fence(50, 50)

    def create_fence(
        self, x, y, width=300, height=200, bg_color=MAGIC_COLOR, border_color="red"
    ):
        fence = Fence(
            self.master, self.next_fence_id, x, y, width, height, bg_color, border_color
        )
        self.fences[self.next_fence_id] = fence
        self.next_fence_id += 1
        return fence

    def create_fence_from_data(self, data):
        fence = Fence(
            self.master,
            data.get("id", self.next_fence_id),
            data["position"]["x"],
            data["position"]["y"],
            data["size"]["width"],
            data["size"]["height"],
            data.get("bg_color", MAGIC_COLOR),
            data.get("border_color", "red"),
        )
        self.fences[data.get("id", self.next_fence_id)] = fence
        self.next_fence_id = max(
            self.next_fence_id, data.get("id", self.next_fence_id) + 1
        )
        return fence

    def add_icon_to_fence(self, icon_widget, fence_id=None):
        if fence_id and fence_id in self.fences:
            fence = self.fences[fence_id]
        else:
            fence = list(self.fences.values())[0]
        fence.add_icon(icon_widget)

    def get_layout(self):
        layout = {"fences": []}
        for fence_id, fence in self.fences.items():
            layout["fences"].append(
                {
                    "id": fence_id,
                    "position": {"x": fence.winfo_x(), "y": fence.winfo_y()},
                    "size": {
                        "width": fence.winfo_width(),
                        "height": fence.winfo_height(),
                    },
                    "bg_color": MAGIC_COLOR,
                    "border_color": "red",
                    "icons": [],  # Future work: save icon positions
                }
            )
        return layout
