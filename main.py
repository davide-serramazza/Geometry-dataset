from color import color_list
from PIL import Image
from generate import generate_example, check_already_generated
from lxml import etree
from helper_functions import check_completion
from dump_results import dump_results

def main():

    n_ex4depth=10 #TODO command line arg
    min_depth = 1
    max_depth = 5
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


if __name__ == "__main__":
    main()
