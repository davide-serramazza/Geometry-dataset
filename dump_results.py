from tqdm import tqdm
import os

def dump_results(examples):
    with open("my_dataset_sentences.txt", "w+") as sen_file:
        for n_figs in examples.keys():
                bucket = examples[n_figs]
                all_dataset_length = len(bucket["imgs"])
                n_test = int(all_dataset_length*0.05)
                print("dump test,val and train of n_figs ",n_figs)
                dump_examples("test",(0,n_test),n_figs, bucket, sen_file)
                dump_examples("val",(n_test,2*n_test),n_figs, bucket, sen_file)
                dump_examples("train",(2*n_test,all_dataset_length  ),n_figs, bucket, sen_file)
    sen_file.close()


def dump_examples(dataset_part,ranges,n_figs, examples, sen_file):
    for i in tqdm(range(ranges[0],ranges[1])):
        name = str(n_figs)+ "_" + str(i).zfill(5)
        sen = examples["sens"][i]
        img = examples["imgs"][i]
        tree_s = examples["tree_strings"][i]
        seg = examples["segs"][i]
        # first plain captions in a single txt files
        sen_file.write(name + " : " + sen + "\n")
        img.save(os.path.join(dataset_part,"images", name + ".png"))
        seg.save(os.path.join(dataset_part,"segmentations", name + ".png"))
        with open(os.path.join(dataset_part,"trees", name + ".xml"), 'w+') as f:
            f.write(tree_s.decode('utf8'))
            f.close()
