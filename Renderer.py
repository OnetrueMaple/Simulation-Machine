import dearpygui.dearpygui as dpg
from time import perf_counter

# The idea so far is to pass an object for the renderer object to render, but the renderer has to handle each type of object according to *that* object's specifications. Methods WIP
class Renderer:

    def __init__(self, window_title="Renderer", allow_frameskipping=False):
        if(not isinstance(window_title, str)):
            raise ValueError("Invalid data type for window_title. Expected 'str', got {window_title}")

        dpg.create_context()

        # Whether or not to allow frame skipping.
        self.allow_frameskipping = allow_frameskipping

        # List of sub-windows inside the main UI window.
        self.windows             = [dpg.add_window(label="Main Canvas", tag="Main Window", width=320, height=240)]

        # List of objects to iterate through and render, 'key: value' is 'window-obj: attribute'
        self.objects             = {}

        dpg.create_viewport(title=window_title, width=640, height=480)
        dpg.set_primary_window(window="Main Window", value=True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_viewport_vsync(False)

    def render_frame(self):
        dpg.render_dearpygui_frame()

    def tick(self):
        self.render_frame()