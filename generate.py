from PIL import ImageDraw
import random
from lxml import etree
from helper_functions import select_current_color, new_cordinate,new_cordinate_circle,is_final_tree_level

def generate_example(spaces,im,segmentaion,root,color_list,depth_range,color_name,sentence):

    draw = ImageDraw.Draw(im)
    seg = ImageDraw.Draw(segmentaion)
    current_depth=0
    last_node=root
    next_level = True

    while next_level:
        s = spaces.pop()

        x1 = s[0]
        x2 = s[2]
        y1 = s[1]
        y2 = s[3]

        shape = random.randint(0, 1)
        color_name, rgb = select_current_color(color_list,color_name)

        if shape == 0:
            # square
            draw.rectangle([x1, y1, x2, y2], width=3, fill=rgb)
            seg.rectangle([x1, y1, x2, y2], width=3, fill=(current_depth+2))
            # update points
            x1, x2, y1, y2 = new_cordinate(x1, x2, y1, y2)
            # update tree
            child = etree.Element('node', color=color_name, shape='square')
            last_node.append(child)
            last_node = child
            # update sentence
            sentence += " a " + color_name + " square"
        else:
            # circle
            draw.ellipse([x1, y1, x2, y2], width=3, fill=rgb)
            seg.ellipse([x1, y1, x2, y2], width=3, fill=(current_depth+2))
            # update points
            x1, x2, y1, y2 = new_cordinate_circle(x1, x2, y1, y2)
            # update tree
            child = etree.Element('node', color=color_name, shape='circle')
            last_node.append(child)
            last_node = child
            # update sentence
            sentence += " a " + color_name + " circle"

        current_depth += 1
        next_level, sentence = is_final_tree_level(x1, y1, x2, y2, sentence,current_depth,depth_range)
        spaces.append((x1, y1, x2, y2))
        current_degree = random.randint(1, 4)

    return sentence, current_depth