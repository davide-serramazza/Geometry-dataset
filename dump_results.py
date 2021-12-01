from tqdm import tqdm
import os

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