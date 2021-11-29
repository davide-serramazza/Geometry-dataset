import math
import random

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
    return  x1+25, x2-25,y1+25,y2-25

def select_current_color( color_list):

    choosed_color = random.randint(0, len(color_list) - 1)
    new_color,rgb = color_list[choosed_color]
    return new_color,rgb

def is_final_tree_level(x1,y1,x2,y2,current_depth,depth_range):
    min_depth = depth_range[0]
    max_depth = depth_range[1]
    if current_depth==(max_depth-1):
        next_level = False
    elif current_depth>=min_depth:
        next_level = (x1+13<x2 and y1+13<y2) and random.random() > 0.5
    else:
        next_level = (x1+13<x2 and y1+13<y2)
    #TODO next step is to try different captions for one image
    #completion = [" containing"]#, " that contains", " which contains", " having inside", " which has"," that has", ]
    #if next_level:
    #    tmp = 0 #random.randint(0,3)
    #    sentence+=completion[tmp]
    return next_level#,sentence

def check_completion(examples,target_num):
    bool = True
    for el in examples.keys():
        bool = bool and len(examples[el]['sens'])==target_num
    return not bool