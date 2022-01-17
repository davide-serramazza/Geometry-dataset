from color import color_list
from generate import generate_example, check_already_generated
from helper_functions import check_completion, init_dict
from dump_results import dump_results

def main():

    n_ex4depth=5 #TODO command line arg
    min_figs = 10
    max_figs = 12
    # data structure for store input and targets
    examples = init_dict(min_figs, max_figs)

    # initialize while condition, number of loop counter and file for "plain" sentences
    to_continue =True
    i=0
    while to_continue:

        # create whire background, initial segmentation map and root of the tree
        ris = generate_example(color_list,min_figs,max_figs)

        if ris!=None:
            sentence,figs_n,im,segmentation,root =ris
            check_already_generated(figs_n, examples, im, n_ex4depth, segmentation, sentence, root)
            # check completion of the loop
            to_continue = check_completion(examples,n_ex4depth)

        # print current filling level of store data structure
        i+=1
        if i%1000==0:
            for n_figs in examples.keys():
                print("\ndepth:",n_figs,":",len(examples[n_figs]["imgs"]))

    # save generated examples
    print("saving")
    dump_results(examples)


if __name__ == "__main__":
    main()
