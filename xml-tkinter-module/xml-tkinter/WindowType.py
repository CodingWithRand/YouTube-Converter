from tkinter import *
from tkinter import ttk
# import xml.etree.ElementTree as ET
from lxml import etree
# from collections import OrderedDict
from additionfuncs import *
from componentPosition import *
from UIConstruction import *
import types
# import re
import ast

all_variables = vars().items()

class MainWindow:
    def __init__(self, window_size=None, original=True):
        self.window = Tk()
        self.window.configure(background=rgb(240, 240, 240))
        if not original:
            self.window_size = window_size
            self.position = win_center_pos(self.window, self.window_size)
        self.Components = {}

    def initiate_window_launch(self, title=None, resizable_tuple=None):
        self.window.title(title)
        self.window.resizable(resizable_tuple[0], resizable_tuple[1])
        if self.position and self.window is not None:
            self.window.geometry(sizing_positioning(self.window_size, self.position))

    def create_component(self, xml_component_list):
        root_components = parsing_XML(xml_component_list)
        all_elem_components = root_components.iterdescendants()
        for component in all_elem_components:
            component_type = component.get('type', default=None)
            font_tuple = (component.get('font', default='TkDefaultFont'), component.get('font-size', default=10))
            bg_color = component.get('background-color', default=rgb(240, 240, 240))
            if component_type == "text":
                component_configurations = Configs(text=component.text, font=font_tuple, bg=bg_color).return_configs()
                for otherComponents in self.Components.values():
                    if component.getparent().tag in otherComponents.get("Parent"):
                        tl = TextLabel(otherComponents.get("Object") , component_configurations)
                    else:
                        continue
                tl = TextLabel(self.window, component_configurations)
                tl.update_template(self.Components, component.tag, component)
            elif component_type == "btn":
                btnStyle = component.get('style', default=None)
                btnCommand, *args = component.get('command', default=None).replace("(", " ").replace(")", "").replace("'", "").replace(",", "").split(" ")
                component_configurations = Configs(text=component.text, font=font_tuple, background=bg_color, btnStyle=btnStyle).return_configs()                
                btn = Btn(self.window, component_configurations)
                all_function_names = {name: obj for name, obj in all_variables if isinstance(obj, types.FunctionType)}
                if btnCommand is not None and btnCommand in all_function_names.keys():
                    btn.add_command(all_function_names[btnCommand], args)
                btn.update_template(self.Components, component.tag, component)
            elif component_type == "frame" or component_type is None:
                frame = WindowFrame(self.window)
                frame.update_template(self.Components, component.tag, component)
            else:
                pass
                # More soon
        # print(self.Components)

    def update_page(self, xml_update_components):
        updating_components = parsing_XML(xml_update_components)
        all_updating_elem_components = updating_components.iterdescendants()
        for key, former_component, updates in zip(self.Components.keys(), self.Components.values(), all_updating_elem_components):
            if key == updates.tag and former_component['Parent'] == updates.getparent().tag:
                former_component["Object"].config(text=updates.text)

    def position_component(self, xml_packing):
        positions_root = parsing_XML(xml_packing)
        positions_list = positions_root.iterdescendants()
        for key, component in self.Components.items():
            for position in positions_list:
                if key == position.tag and component['Parent'] == position.getparent().tag:
                    position_component(component["Object"], *record_position_from_attrib({
                        "objAttrib": position.attrib,
                        "positionAttrib": position.find('Pos').iterdescendants() if position.find('Pos') is not None else None
                    }))
                    break
            # print(key, component['Parent'])

    def complete_setup(self):
        self.window.mainloop()

def test(man, woman, *n):
    print(f"[{man}]: I love you {woman}")
    print(f"[{woman}]: Me too baby.")
    for i in n:
        print(i)

win = MainWindow(window_size=(700, 500), original=False)
win.initiate_window_launch(title="Welcome to our program!", resizable_tuple=(FALSE, FALSE))
win.create_component(
    '''
        <tkinter>
            <Head type="text" font="Georgia" font-size="30">Thank you for choosing our program</Head>
            <Subtitle type="text" font="Calibri Light" font-size="18">Now, we're going to introduce you how to use this program</Subtitle>
            <Content>
                <Paragraphs>
                    <paragraph-1 type="text" font="Calibri Light" font-size="16">First of all, this program is used for cleaning up specific folders before shutdown
your computer. That could clear up some of your disk space. You can choose any
folders you want to delete!</paragraph-1>
                    <paragraph-2 type="text" font="Calibri Light" font-size="16">In the next page, you'll be choosing the folders to get cleaned up before 
shutdown your computer. There are several folders that has been selected as 
suggestion folders already. You shouldn't unselect it. But if you want, it's 
up to you. You can configure the folders to get cleaned up again</paragraph-2>
                </Paragraphs>
                <NextBtn type="btn" style="modern" command="test('Rand0M', 'Carisa', [1, 2, 2, 3, 4, 12, 3, 5])">Next</NextBtn>
            </Content>
        </tkinter>
    '''
)
win.position_component(
    '''
        <tkinter>
            <Head display="flex">
                <Pos>
                    <Margin-Y>10</Margin-Y>
                </Pos>
            </Head>
            <Subtitle display="flex">
                <Pos>
                    <Margin-Y>8</Margin-Y>
                </Pos>
            </Subtitle>
            <Content display="flex">
                <Pos />
                <Paragraphs display="flex">
                    <Pos />
                    <paragraph-1 display="flex">
                        <Pos>
                            <Margin-Y>4</Margin-Y>
                        </Pos>
                    </paragraph-1>
                    <paragraph-2 display="flex">
                        <Pos>
                            <Margin-Y>4</Margin-Y>
                        </Pos>
                    </paragraph-2>
                </Paragraphs>
                <NextBtn display="flex">
                    <Pos>
                        <Padding-Y>5</Padding-Y>
                        <Padding-X>10</Padding-X>
                        <Margin-Y>80 0</Margin-Y>
                    </Pos>
                </NextBtn>
            </Content>
        </tkinter>
    '''
)

win.complete_setup()

