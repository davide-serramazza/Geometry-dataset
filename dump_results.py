from tqdm import tqdm
import os

def dump_results(examples):
    with open("my_dataset_sentences.txt", "w+") as sen_file:
        for depth in examples.keys():
            for b in examples[depth]["breaths"]:
                bucket = examples[depth]["breaths"][b]
                all_dataset_length = len(bucket["imgs"])
                n_test = int(all_dataset_length*0.05)
                print("dump test,val and train of depth",depth,"breath",b)
                dump_examples("test",(0,n_test),depth, bucket, sen_file,b)
                dump_examples("val",(n_test,2*n_test),depth, bucket, sen_file,b)
                dump_examples("train",(2*n_test,all_dataset_length  ),depth, bucket, sen_file,b)
    sen_file.close()


def dump_examples(dataset_part,ranges,depth, examples, sen_file,breath):
    for i in tqdm(range(ranges[0],ranges[1])):
        name = str(depth)+ "_" +str(breath)+ "_" + str(i).zfill(5)
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
