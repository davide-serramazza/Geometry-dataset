import argparse
from color import color_list
from generate import generate_example
from helper_functions import check_already_generated, init_dict
from dump_results import dump_results

def main():

    #argument parse
    parser = argparse.ArgumentParser()
    parser.add_argument('min_figs', type=int, help='minimum number of figures per image')
    parser.add_argument('max_figs',type=int, help="maximum number of figures per image")
    parser.add_argument('n_ex4figs_n',type=int, help="number of different example to generate per figure number")
    args = parser.parse_args()
    n_ex4figs_n=args.n_ex4figs_n
    min_figs = args.min_figs
    max_figs = args.max_figs

    # data structure for store input and targets
    examples = init_dict(min_figs, max_figs)

    # initialize while condition, number of loop counter and file for "plain" sentences
    for j in range(min_figs,max_figs+1):
        i=0
        while len(examples[j]["imgs"]) < n_ex4figs_n:

            ris = generate_example(color_list,j)
            if ris!=None:
                sentence,figs_n,im,segmentation,root = ris
                check_already_generated(figs_n, examples, im, n_ex4figs_n, segmentation, sentence, root)

            # print how much are already generated
            i+=1
            if i%1000==0:
                for n_figs in examples.keys():
                    print("\ndepth:",n_figs,":",len(examples[n_figs]["imgs"]))

    # save generated examples
    print("saving")
    dump_results(examples)


if __name__ == "__main__":
    main()
