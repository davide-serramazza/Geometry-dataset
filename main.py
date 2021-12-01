from color import color_list
from PIL import Image
from generate import generate_example
from lxml import etree
from helper_functions import check_completion
import os
from tqdm import tqdm

def main():

    n_ex4depth=7500 #TODO command line arg
    min_depth = 1
    max_depth = 2
    min_breadth = 1
    max_breadth=3
    depth_range = (min_depth,max_depth) #TODO coomand line arg
    breadth_range = (min_breadth,max_breadth)
    # data structure for store input and targets
    examples =  dict.fromkeys( [i for i in range(min_depth,max_depth)])
    for el in examples.keys():
        examples[el]  ={"imgs": [], "sens": [],"tree_strings" : [], "segs":[]}

    # initialize while condition, number of loop counter and file for "plain" sentences
    to_continue =True
    i=0
    while to_continue:

        # create whire background, initial segmentation map and root of the tree
        im = Image.new('RGB', (550, 550), (255,255,255))
        segmentation =  Image.new('L', (550, 550), (0))
        root = etree.Element("root",label=str(0))

        x1=0; x2=550; y1=0; y2=550         #TODO togliere costanti
        spaces = [(x1,y1,x2,y2)]
        sentence,depth = generate_example(spaces,im,segmentation,root,color_list,depth_range,breadth_range)

        check_already_generated(depth, examples, im, n_ex4depth, segmentation, sentence, root)
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
    dump_results(examples)


def dump_results(examples):
    with open("my_dataset_sentences.txt", "w+") as sen_file:
        for depth in examples.keys():
            for i in tqdm(range(len(examples[depth]["sens"]))):
                name = str(depth).zfill(3) + "_" + str(i).zfill(4)
                sen = examples[depth]["sens"][i]
                img = examples[depth]["imgs"][i]
                tree_s = examples[depth]["tree_strings"][i]
                seg = examples[depth]["segs"][i]
                # first plain captions in a single txt files
                sen_file.write(name + " : " + sen + "\n")
                img.save(os.path.join("images", name + ".png"))
                img.convert('L').save(os.path.join("grays", name + ".png"))
                seg.save(os.path.join("segmentations", name + ".png"))
                with open(os.path.join("trees", name + ".xml"), 'w+') as f:
                    f.write(tree_s.decode('utf8'))
                f.close()
    sen_file.close()


def check_already_generated(depth, examples, im, n_ex4depth, segmentation, sentence, root):
    tree_string = etree.tostring(root, pretty_print=True)
    # check if already generated
    bucket = examples[depth]
    if tree_string not in bucket["tree_strings"] and len(bucket["sens"]) < n_ex4depth:
        bucket["tree_strings"].append(tree_string)
        bucket["imgs"].append(im)
        bucket["sens"].append(sentence)
        bucket["segs"].append(segmentation)


if __name__ == "__main__":
    main()
