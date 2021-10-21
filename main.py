from color import color_list
from PIL import Image
from generate import generate_example
from lxml import etree
from helper_functions import check_completion, select_current_color
import os
from tqdm import tqdm

def main():

    n_ex4depth=2000 #TODO command line arg
    min_depth = 5
    max_depth = 11
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
        background_color,rgb = select_current_color(color_list,"")
        im = Image.new('RGB', (550, 550), rgb)
        initial_sentene = "A "+background_color+ " background and"

        # initialize tree sentence and current color
        root = etree.Element("background", color="Black")

        # keep track of depth and breadth, current coordinates and a tree and a sentence as targets
        #TODO togliere costanti
        x1 = 12
        x2= 538
        y1= 12
        y2= 538
        spaces = [(x1,y1,x2,y2)]
        sentence,depth = generate_example(spaces,im,root,color_list,depth_range,background_color,initial_sentene)
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
    print("saving")
    with open("my_dataset_sentences.txt","w+") as sen_file:
        for depth in examples.keys():
            for i in tqdm(range(len(examples[depth]["sens"]))):
                name = str(depth).zfill(3)+"_"+str(i).zfill(4)
                sen = examples[depth]["sens"][i]
                img = examples[depth]["imgs"][i]
                tree_s = examples[depth]["tree_strings"][i]
                # first plain captions in a single txt files
                sen_file.write(name+" : "+sen+"\n")
                img.save(os.path.join("images",name+".png"))
                img.convert('L').save(os.path.join("grays",name+".png"))
                with open(os.path.join("trees",name+".xml"),'w+') as f:
                    f.write(tree_s.decode('utf8'))
                f.close()
    sen_file.close()


if __name__ == "__main__":
    main()