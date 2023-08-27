from tkinter import *
from tkinter import ttk
from additionfuncs import *


def pseudo_function(): pass


class Configs:
    def __init__(self, **configs):
        self.configs = configs
        # More #
    
    def return_configs(self):
        return self.configs
    

class TextLabel:
    def __init__(self, rootWindow, configs):
        self.TL = Label(rootWindow, **configs)
    
    def update_template(self, template_dict, xml_component_tag, xml_component):
        update_component_dict(template_dict, xml_component_tag, xml_component, self.TL)


class Btn:
    def __init__(self, rootWindow, configs):
        style = configs.pop("btnStyle")
        if style == "modern":
            btnText = configs.pop("text")
            ttk.Style().configure("btnStyle.TButton", **configs)
            self.btn = ttk.Button(rootWindow, text=btnText, style="btnStyle.TButton")
        elif style in ["default", None]:
            self.btn = Button(rootWindow, **configs)
    
    def add_command(self, cmd, args):
        self.btn.configure(command=lambda: cmd(*args))
    
    def update_template(self, template_dict, xml_component_tag, xml_component):
        update_component_dict(template_dict, xml_component_tag, xml_component, self.btn)


class WindowFrame:
    def __init__(self, rootWindow):
        self.frame = Frame(rootWindow)
    
    def update_template(self, template_dict, xml_component_tag, xml_component):
        update_component_dict(template_dict, xml_component_tag, xml_component, self.frame)    

