from color import color_list
from PIL import Image
from generate import generate_example
from lxml import etree
from helper_functions import check_completion

import os

def main():

    exemples =  dict.fromkeys( [i for i in range(7,13)])
    for el in exemples.keys():
        exemples[el]  ={"imgs": [], "trees": [], "sens": set(),"parsed_sens" : []}

    exemples_for_depth=1000
    to_continue =True

    while to_continue:
        # create black background
        im = Image.new('RGB', (1000, 1000), (0, 0, 0))

        # initialize tree sentence and current color
        root = etree.Element("background", color="Black")

        # keep track of depth and breadth, current coordinates and a tree and a sentence as targets
        x1 = 25
        x2= 975
        y1= 25
        y2= 975
        spaces = [(x1,y1,x2,y2)]
        sentence,depth = generate_example(spaces,im,root,color_list)
        tree_string = etree.tostring(root, pretty_print=True)

        # check if already generated
        bucket = exemples[depth]
        if tree_string not in bucket["sens"] and len(bucket["sens"]) < exemples_for_depth:
            bucket["sens"].add(tree_string)
            bucket["imgs"].append(im)
            bucket["trees"].append(tree_string)
        else:
            print("NOOOOOOOOOO")

        for el in exemples.keys():
            print(el,":",len(exemples[el]["sens"]),end=";")
        print("\n")
        to_continue = check_completion(exemples,exemples_for_depth)
        #with open("tree.xml","w+") as f:
            #f.write((tree_string).decode('utf8'))
        #im.save("image.png")





if __name__ == "__main__":
    main()