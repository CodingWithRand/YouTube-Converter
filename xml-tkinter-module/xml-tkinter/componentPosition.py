from tkinter import *
from tkinter import ttk

def record_position_from_attrib(xml_attribs):
    # ------------ Style data store ------------ #

    flexibility, gridity, fixed = None, None, None
    responsive = None
    alignment = None
    padding_y, padding_x = 0, 0
    margin_y, margin_x = 0, 0

    # ------------------------------------------ #

    for obj_attrib_key, obj_attrib_value in xml_attribs["objAttrib"].items():
        # Display style
        if obj_attrib_key == "display":
            if obj_attrib_value == "flex":
                flexibility = True
            elif obj_attrib_value == "grid":
                gridity = True
            elif obj_attrib_value == "fixed":
                fixed = True
            else:
                pass

        # Responsive
        if obj_attrib_key == "responsive":
            responsive = bool(obj_attrib_value)

        if obj_attrib_key == "align":
            if obj_attrib_value == "center":
                alignment = "center"
    
    if xml_attribs["positionAttrib"] is not None:
        for pos in xml_attribs["positionAttrib"]:
            component_position = tuple(int(num) for num in pos.text.split(" "))
            if len(component_position) < 2:
                component_position = pos.text
                
            
            if pos.tag == "Padding-Y":
                padding_y = component_position
            elif pos.tag == "Padding-X":
                padding_x = component_position
            elif pos.tag == "Margin-Y":
                margin_y = component_position
            elif pos.tag == "Margin-X":
                margin_x = component_position


    style_data_list = {
        "flexibility": flexibility, 
        "gridity": gridity, 
        "fixed": fixed, 
        "responsive": responsive, 
        "alignment": alignment

    }
    pack_list = {
        "ipadx": padding_x,
        "ipady": padding_y,
        "padx": margin_x,
        "pady": margin_y
    }

    return style_data_list, pack_list

def position_component(givenComponent, style, general_position):
    if style["flexibility"]: 
        if style["responsive"] and style["alignment"] == "center":
            givenComponent.pack(
                # General position attribute #
                **general_position,
                # Responsive # 
                fill=BOTH, 
                expand=True
            )
        else:
            givenComponent.pack(
                # General position attribute #
                **general_position
            )
        # print(general_position)

            