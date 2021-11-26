from PIL import ImageDraw
import random
import numpy as np
from lxml import etree
from helper_functions import select_current_color, new_cordinate,new_cordinate_circle,is_final_tree_level

def generate_example(spaces,im,segmentaion,root,color_list,depth_range,sentence):

    draw = ImageDraw.Draw(im)
    seg = ImageDraw.Draw(segmentaion)
    current_depth=0
    current_fig_n=1
    last_node=root
    next_level = True
    new_spaces = []
    while next_level:
        for s in spaces:
            x1 = s[0];x2 = s[2];y1 = s[1];y2 = s[3]
            currents_quarter = [(x1, y1 , x1+(x2-x1)/2 , y1+(y2-y1)/2),
                                ( x1+(x2-x1)/2 ,y1 , x2 , y1+(y2-y1)/2),
                                (x1, y1+(y2-y1)/2 , x1+(x2-x1)/2 ,y2),
                                ( x1+(x2-x1)/2, y1+(y2-y1)/2 ,x2,y2)]
            current_breadth = random.randint(1, 4)
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
                    child = etree.Element('node', color=color_name, shape='square')
                    last_node.append(child)
                    # update sentence
                    sentence += " a " + color_name + " square"
                else:
                    # circle
                    draw.ellipse([x1-3, y1-3, x2-3, y2-3], width=2, fill=rgb, outline=(0,0,0))
                    seg.ellipse([x1-3, y1-3, x2-3, y2-3], width=2, fill=(current_fig_n))
                    # update points
                    x1, x2, y1, y2 = new_cordinate_circle(x1, x2, y1, y2)
                    # update tree
                    child = etree.Element('node', color=color_name, shape='circle')
                    last_node.append(child)
                    # update sentence
                    sentence += " a " + color_name + " circle"
                new_spaces.append( (x1,y1,x2,y2) )
                current_fig_n+=1

        spaces = new_spaces
        new_spaces = []
        current_depth += 1
        next_level, sentence = is_final_tree_level(x1, y1, x2, y2, sentence,current_depth,depth_range)

    return sentence, current_depth