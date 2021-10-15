from color import color_list
from PIL import Image
from generate import generate_example
from lxml import etree
from helper_functions import check_completion
from os.path import join
import os

def main():

    os.mkdir("trees")
    os.mkdir("images")
    # data structure for store input and targets
    examples =  dict.fromkeys( [i for i in range(7,13)])
    for el in examples.keys():
        examples[el]  ={"imgs": [], "trees": [], "sens": set(),"parsed_sens" : []}

    n_ex4depth=5 #TODO command line arg

    # initialize while condition, number of loop counter and file for "plain" sentences
    to_continue =True
    i=0
    plain_sentences = open("senteces.txt","w+")
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
        bucket = examples[depth]
        if tree_string not in bucket["trees"] and len(bucket["sens"])<n_ex4depth:
            bucket["sens"].add(sentence)
            bucket["imgs"].append(im)
            bucket["trees"].append(tree_string)

        # check completion of the task and save the current generated sample
        to_continue = check_completion(examples,n_ex4depth)

        name = str(depth)+"_"+str(len(bucket["trees"]))
        with open(join("trees",name+".xml"),"w+") as f:
            f.write((tree_string).decode('utf8'))
        im.save(join("images",name+".png"))
        plain_sentences.write(name+" : "+sentence)

        # print current filling level of store data structure
        i+=1
        if i%100==0:
            for el in examples.keys():
                print(el,":",len(examples[el]["sens"]),end=";\t")
            print("\n")





if __name__ == "__main__":
    main()