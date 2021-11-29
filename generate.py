from PIL import ImageDraw
import random
import numpy as np
from lxml import etree
from helper_functions import select_current_color, new_cordinate,new_cordinate_circle,is_final_tree_level

def generate_sentence(tree):
    sentence=""
    for node in tree:
        completion = [" containing"]#, " that contains", " which contains", " having inside", " which has"," that has", ]
        tmp = 0 #random.randint(0,3)
        to_use = completion[tmp]
        sentence+="a " + node.attrib["color"]+" "+node.attrib["shape"]+" "+to_use+" "+str(len(node.getchildren()))+" other shapes and "
    return sentence[:-5]

def generate_example(spaces,im,segmentaion,root,color_list,depth_range,breadth_range):

    draw = ImageDraw.Draw(im)
    seg = ImageDraw.Draw(segmentaion)
    current_depth=0
    current_fig_n=1
    nodes=[root]
    next_level = True
    next_level_data = {"areas":[],"subtrees":[]}
    while next_level:
        for (s,last_node) in zip(spaces,nodes):
            x1 = s[0];x2 = s[2];y1 = s[1];y2 = s[3]
            currents_quarter = [(x1, y1 , x1+(x2-x1)/2 , y1+(y2-y1)/2),
                                ( x1+(x2-x1)/2 ,y1 , x2 , y1+(y2-y1)/2),
                                (x1, y1+(y2-y1)/2 , x1+(x2-x1)/2 ,y2),
                                ( x1+(x2-x1)/2, y1+(y2-y1)/2 ,x2,y2)]
            current_breadth = random.randint(breadth_range[0], breadth_range[1])
            quarter_priority= np.random.permutation(4)
            for i in range(current_breadth):
                current_quarter = currents_quarter[quarter_priority[i]]
                x1 = current_quarter[0];x2 = current_quarter[2];y1 = current_quarter[1];y2 = current_quarter[3]
                shape = random.randint(0, 1)
                color_name, rgb = select_current_color(color_list)

                if shape == 0:
                    # square
                    draw.rectangle([x1-3, y1-3, x2-3, y2-3], width=2, fill=rgb,outline=(0,0,0))
                    seg.rectangle([x1-3, y1-3, x2-3, y2-3], width=2, fill=(current_fig_n))
                    # update points
                    x1, x2, y1, y2 = new_cordinate(x1, x2, y1, y2)
                    # update tree
                    child = etree.Element('node', color=color_name, shape='square',label=str(current_fig_n))
                    last_node.append(child)
                    # update sentence
                else:
                    # circle
                    draw.ellipse([x1-3, y1-3, x2-3, y2-3], width=2, fill=rgb, outline=(0,0,0))
                    seg.ellipse([x1-3, y1-3, x2-3, y2-3], width=2, fill=(current_fig_n))
                    # update points
                    x1, x2, y1, y2 = new_cordinate_circle(x1, x2, y1, y2)
                    # update tree
                    child = etree.Element('node', color=color_name, shape='circle',label=str(current_fig_n))
                    last_node.append(child)
                    # update sentence
                next_level_data["areas"].append( (x1,y1,x2,y2) )
                next_level_data["subtrees"].append(child)
                current_fig_n+=1

        current_depth += 1
        next_level = is_final_tree_level(x1, y1, x2, y2,current_depth,depth_range)
        spaces = next_level_data["areas"]
        next_level_data["areas"] = []
        nodes = next_level_data["subtrees"]
        next_level_data["subtrees"] = []

    sentence = generate_sentence(root.getchildren())
    return sentence, current_depth