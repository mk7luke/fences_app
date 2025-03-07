# fences.py
import tkinter as tk


class Fence(tk.Frame):
    def __init__(
        self,
        master,
        fence_id,
        x,
        y,
        width=300,
        height=200,
        bg_color="#ffffff",
        border_color="#000000",
        transparency=1.0,
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            bg=bg_color,
            highlightbackground=border_color,
            highlightthickness=2,
            **kwargs
        )
        self.fence_id = fence_id
        self.place(x=x, y=y)
        self.icons = []  # List to hold icon widgets within the fence

        # Bind mouse events for dragging the fence
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self._drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_drag(self, event):
        # Calculate the new position and update the placement of the fence
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        new_x = self.winfo_x() + dx
        new_y = self.winfo_y() + dy
        self.place(x=new_x, y=new_y)

    def stop_drag(self, event):
        self._drag_data = {"x": 0, "y": 0}

    def add_icon(self, icon_widget):
        # Add an icon to the fence
        icon_widget.master = self  # Change parent to the fence
        self.icons.append(icon_widget)
        # Place icon at its current coordinates (or update based on desired logic)
        icon_widget.place(x=icon_widget.winfo_x(), y=icon_widget.winfo_y())


class FenceManager:
    def __init__(self, master, layout_data=None):
        self.master = master
        self.fences = {}
        self.next_fence_id = 1
        if layout_data and "fences" in layout_data:
            for fence_data in layout_data["fences"]:
                self.create_fence_from_data(fence_data)
        else:
            # Create a default fence if no layout exists
            self.create_fence(50, 50)

    def create_fence(
        self,
        x,
        y,
        width=300,
        height=200,
        bg_color="#ffffff",
        border_color="#000000",
        transparency=1.0,
    ):
        fence = Fence(
            self.master,
            self.next_fence_id,
            x,
            y,
            width,
            height,
            bg_color,
            border_color,
            transparency,
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
            data.get("bg_color", "#ffffff"),
            data.get("border_color", "#000000"),
            data.get("transparency", 1.0),
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
            # If no specific fence is mentioned, add the icon to the first fence created
            fence = list(self.fences.values())[0]
        fence.add_icon(icon_widget)

    def get_layout(self):
        # Gather layout data for each fence to be saved in a JSON file
        layout = {"fences": []}
        for fence_id, fence in self.fences.items():
            fence_data = {
                "id": fence_id,
                "position": {"x": fence.winfo_x(), "y": fence.winfo_y()},
                "size": {"width": fence.winfo_width(), "height": fence.winfo_height()},
                "bg_color": fence["bg"],
                "border_color": fence["highlightbackground"],
                "transparency": 1.0,  # Tkinter does not directly support transparency for Frames
                "icons": [],  # Icons data could be added here if needed
            }
            layout["fences"].append(fence_data)
        return layout
