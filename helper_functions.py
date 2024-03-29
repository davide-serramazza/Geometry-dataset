import math
import random
from lxml import etree
from PIL import Image
import copy

def init_dict(min_figs, max_figs):
    examples = dict.fromkeys([i for i in range(min_figs, max_figs+1)])
    for n_figs in examples.keys():
        buckets = {"imgs": [], "sens": [], "tree_strings": [], "segs": []}
        examples[n_figs] = copy.deepcopy(buckets)
    return examples

def select_current_color( color_list, parent_color):

    choosed_color = parent_color
    while choosed_color==parent_color:
        idx = random.randint(0, len(color_list) - 1)
        choosed_color = color_list [idx]
    new_color,rgb = choosed_color
    return new_color,rgb

def update_for_next_level(next_level_data):
    spaces = next_level_data["areas"]
    next_level_data["areas"] = []
    nodes = next_level_data["subtrees"]
    next_level_data["subtrees"] = []
    parent_colors = next_level_data["parent_color"]
    next_level_data["parent_color"] = []
    return spaces,nodes,parent_colors

def new_cordinate_circle(x1, x2, y1, y2):
    center_x = (x2 + x1) / 2
    center_y = (y2+y1) /2
    radius = (x2-x1) /2
    sin_cos = radius * math.sqrt(2) / 2
    x1 = center_x - sin_cos
    x2 = center_x + sin_cos
    y1 = center_y - sin_cos
    y2 = center_y + sin_cos

    #print(s, x1, x2, y1, y2)
    return x1, x2, y1, y2

def new_cordinate(x1,x2,y1,y2):
    min_space = 7
    return  x1+min_space, x2-min_space,y1+min_space,y2-min_space

def draw_circle(color_name, current_fig_n, draw, last_node, rgb, seg, x1, x2, y1, y2,quarter):
    draw.ellipse([x1 - 3, y1 - 3, x2 - 3, y2 - 3], width=2, fill=rgb, outline=(0, 0, 0))
    seg.ellipse([x1 - 3, y1 - 3, x2 - 3, y2 - 3], width=2, fill=(current_fig_n))
    # update points
    x1, x2, y1, y2 = new_cordinate_circle(x1, x2, y1, y2)
    # update tree
    child = etree.Element('node', color=color_name, shape='circle', label=str(current_fig_n),quarter=str(quarter) )
    last_node.append(child)
    return child, x1, x2, y1, y2


def draw_square(color_name, current_fig_n, draw, last_node, rgb, seg, x1, x2, y1, y2,quarter):
    draw.rectangle([x1 - 3, y1 - 3, x2 - 3, y2 - 3], width=2, fill=rgb, outline=(0, 0, 0))
    seg.rectangle([x1 - 3, y1 - 3, x2 - 3, y2 - 3], width=2, fill=(current_fig_n))
    # update points
    x1, x2, y1, y2 = new_cordinate(x1, x2, y1, y2)
    # update tree
    child = etree.Element('node', color=color_name, shape='square', label=str(current_fig_n),quarter=str(quarter) )
    last_node.append(child)
    return child, x1, x2, y1, y2

def initialize_new_blank_image():
    im = Image.new('RGB', (550, 550), (255, 255, 255))
    segmentation = Image.new('L', (550, 550), (0))
    root = etree.Element("root", color="white", label=str(0))
    x1 = 0; x2 = 550; y1 = 0; y2 = 550  # TODO togliere costanti
    spaces = [(x1, y1, x2, y2)]
    return im, root, segmentation, spaces


def check_already_generated(figs_n, examples, im, n_ex4figs_n, segmentation, sentence, root):
    tree_string = etree.tostring(root, pretty_print=True)
    # check if already generated
    bucket = examples[figs_n]
    if tree_string not in bucket["tree_strings"] and len(bucket["imgs"]) < n_ex4figs_n:
        bucket["tree_strings"].append(tree_string)
        bucket["imgs"].append(im)
        bucket["sens"].append(sentence)
        bucket["segs"].append(segmentation)
