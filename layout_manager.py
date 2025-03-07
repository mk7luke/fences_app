# layout_manager.py
import json
import os


class LayoutManager:
    def __init__(self, config_file):
        self.config_file = config_file

    def load_layout(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    return data
            except Exception as e:
                print("Error loading layout:", e)
        # Return an empty layout if no configuration exists
        return {}

    def save_layout(self, layout):
        try:
            with open(self.config_file, "w") as f:
                json.dump(layout, f, indent=4)
        except Exception as e:
            print("Error saving layout:", e)
