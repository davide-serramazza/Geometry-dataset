from color import color_list
from PIL import Image
from generate import generate_example
from lxml import etree
from helper_functions import check_completion
import os

def main():

    n_ex4depth=1000 #TODO command line arg
    min_depth = 5
    max_depth = 10
    depth_range = (min_depth,max_depth) #TODO coomand line arg
    # data structure for store input and targets
    examples =  dict.fromkeys( [i for i in range(min_depth,max_depth)])
    for el in examples.keys():
        examples[el]  ={"imgs": [], "sens": [],"tree_strings" : [] }


    # initialize while condition, number of loop counter and file for "plain" sentences
    to_continue =True
    i=0
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
        sentence,depth = generate_example(spaces,im,root,color_list,depth_range)
        tree_string = etree.tostring(root, pretty_print=True)

        # check if already generated
        bucket = examples[depth]
        if tree_string not in bucket["tree_strings"] and len(bucket["sens"])<n_ex4depth:
            bucket["tree_strings"].append(tree_string)
            bucket["imgs"].append(im)
            bucket["sens"].append(sentence)

        # check completion of the loop
        to_continue = check_completion(examples,n_ex4depth)

        # print current filling level of store data structure
        i+=1
        if i%1000==0:
            for el in examples.keys():
                print(el,":",len(examples[el]["sens"]),end=";\t")
            print("\n")

    # save generated examples
    with open("my_dataset_sentences.txt","w+") as sen_file:
        for depth in examples.keys():
            for i in range(len(examples[depth]["sens"])):
                name = str(depth)+"_"+str(i)
                sen = examples[depth]["sens"][i]
                img = examples[depth]["imgs"][i]
                tree_s = examples[depth]["tree_strings"][i]
                # first plain captions in a single txt files
                sen_file.write(name+" : "+sen+"\n")
                img.save(os.path.join("images",name+".png"))
                with open(os.path.join("trees",name+".xml"),'w+') as f:
                    f.write(tree_s.decode('utf8'))
                f.close()
    sen_file.close()
    # images



if __name__ == "__main__":
    main()