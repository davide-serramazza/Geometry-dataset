from PIL import ImageDraw
import random
import numpy as np
from lxml import etree
from helper_functions import select_current_color, draw_circle, draw_square,initialize_new_blank_image

def generate_example(color_list,figs2gen):

    im, root, segmentation, spaces = initialize_new_blank_image()
    # initialize variables to use in the loop
    draw = ImageDraw.Draw(im)
    seg = ImageDraw.Draw(segmentation)
    current_depth=0
    current_fig_n=0
    nodes=[root]
    parent_colors = ["white"]
    next_level = True
    next_level_data = {"areas":[],"subtrees":[],"parent_color":[]}
    # while other level need to be generated
    while next_level :
        for (s,last_node,parent_c) in zip(spaces,nodes,parent_colors):
            # for each of the nodes in the upper level choose the arity of the node i.e. generate children at
            # current level
            current_breadth, currents_quarter, quarter_priority = select_current_arity(s)
            current_level_figures = []
            for i in range(current_breadth):
                # for each child select current shape and color
                selected_quarter = currents_quarter[quarter_priority[i]]
                x1 = selected_quarter[0];x2 = selected_quarter[2];y1 = selected_quarter[1];y2 = selected_quarter[3]
                # check if the same shape is in the current level
                color_name, rgb, shape = check_current_level(color_list, current_level_figures,last_node,parent_c)

                if shape == 0:      # square
                    child, x1, x2, y1, y2 = draw_square(color_name, current_fig_n, draw, last_node, rgb, seg, x1, x2,y1, y2,quarter_priority[i])
                else:               # circle
                    child, x1, x2, y1, y2 = draw_circle(color_name, current_fig_n, draw, last_node, rgb, seg, x1, x2, y1, y2,quarter_priority[i])

                next_level_data["areas"].append( (x1,y1,x2,y2) )
                next_level_data["subtrees"].append(child)
                next_level_data["parent_color"].append(color_name)
                current_fig_n+=1
                if current_fig_n == figs2gen:
                    sentence = generate_sentence(root.getchildren())
                    print(current_fig_n)
                    return sentence, current_fig_n,im,segmentation,root

        # if conditions are met choose if a new level must be generated and in this case update data structure for
        # the next iteration
        current_depth += 1
        next_level = current_depth < 3
        #next_level = is_final_tree_level(x1, y1, x2, y2,current_depth,depth_range)
        if next_level:  #TODO move in is_final_tree_level function
            spaces = next_level_data["areas"]
            next_level_data["areas"] = []
            nodes = next_level_data["subtrees"]
            next_level_data["subtrees"] = []
            parent_colors = next_level_data["parent_color"]
            next_level_data["parent_color"] = []

    # finally generate sentence #TODO generate the input tree and target sentence and tree??
    return None


def check_current_level(color_list, current_level_figures,last_node,parent_color):
    already_present = True
    while already_present:
        shape = random.randint(0, 1)
        color_name, rgb = select_current_color(color_list,last_node.attrib["color"])
        while color_name==parent_color:
            color_name, rgb = select_current_color(color_list,last_node.attrib["color"])
        current_figure = (shape, color_name)
        already_present = current_figure in current_level_figures
        current_level_figures.append(current_figure)
    return color_name, rgb, shape

def select_current_arity(s):
    x1 = s[0];x2 = s[2];y1 = s[1];y2 = s[3]
    currents_quarter = [(x1, y1, x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2),
                        (x1 + (x2 - x1) / 2, y1, x2, y1 + (y2 - y1) / 2),
                        (x1, y1 + (y2 - y1) / 2, x1 + (x2 - x1) / 2, y2),
                        (x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2, x2, y2)]
    current_breadth = random.randint(1,4)
    quarter_priority = np.random.permutation(4)
    return current_breadth, currents_quarter, quarter_priority

def check_already_generated(figs_n, examples, im, n_ex4depth, segmentation, sentence, root):
    tree_string = etree.tostring(root, pretty_print=True)
    # check if already generated
    bucket = examples[figs_n]
    if tree_string not in bucket["tree_strings"] and len(bucket["imgs"]) < n_ex4depth:
        bucket["tree_strings"].append(tree_string)
        bucket["imgs"].append(im)
        bucket["sens"].append(sentence)
        bucket["segs"].append(segmentation)

def generate_sentence(tree):
    sentence=""
    completion = ["containing"]#, " that contains", " which contains", " having inside", " which has"," that has", ]
    first_level_n = len(tree)

    for i in range(first_level_n):
        tree.append(tree[i].getchildren())

    i=0
    for node in tree:
        if type(node)==etree._Element:
            sentence+="and a " + node.attrib["color"]+" "+node.attrib["shape"]+" "
        elif type(node)==list and node!=[]:
            if sentence.count(":")==0:
                sentence+=": "
            d = { 0 : "first one", 1 : "second one", 2 : "third one" , 3 : "fourth one"}
            tmp = 0 #random.randint(0,len(completion))
            to_use = completion[tmp]
            sentence+= "the "+d[i] +" " +to_use+" "
            for child in node:
                grandchild = len(child.getchildren())
                if child!=node[0]:
                    sentence+="and "
                sentence+="a " + child.attrib["color"]+" "+child.attrib["shape"]+ " in turn "+to_use+ " " + str(grandchild)+" other shapes "
            sentence=sentence[:-1]+"; "
            i+=1
    if tree[-1]==[] :
        return sentence[4:-1]
    else:
        return sentence[4:-2]
