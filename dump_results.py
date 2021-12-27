from tqdm import tqdm
import os

def dump_results(examples):
    with open("my_dataset_sentences.txt", "w+") as sen_file:
        for depth in examples.keys():
            all_dataset_length = len(examples[depth]["imgs"])
            n_test = int( len(examples[depth]["imgs"])*0.05 )
            dump_examples("test",(0,n_test),depth, examples, sen_file)
            dump_examples("val",(n_test,2*n_test),depth, examples, sen_file)
            dump_examples("train",(2*n_test,all_dataset_length  ),depth, examples, sen_file)
    sen_file.close()


def dump_examples(dataset_part,ranges,depth, examples, sen_file):
    for i in tqdm(range(ranges[0],ranges[1])):
        name = str(depth).zfill(3) + "_" + str(i).zfill(5)
        sen = examples[depth]["sens"][i]
        img = examples[depth]["imgs"][i]
        tree_s = examples[depth]["tree_strings"][i]
        seg = examples[depth]["segs"][i]
        # first plain captions in a single txt files
        sen_file.write(name + " : " + sen + "\n")
        img.save(os.path.join(dataset_part,"images", name + ".png"))
        seg.save(os.path.join(dataset_part,"segmentations", name + ".png"))
        with open(os.path.join(dataset_part,"trees", name + ".xml"), 'w+') as f:
            f.write(tree_s.decode('utf8'))
            f.close()