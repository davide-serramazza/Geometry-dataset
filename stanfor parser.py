import os

with open("my_dataset_sentences.txt", "r") as f:
    sentences = f.readlines()

new_dir = "/home/davide/stanford_parser/"
os.chdir(new_dir)
command = "java -mx500m -cp ./*: edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat xmlTree edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"
for el in sentences:
    tmp = el.split(" : ")
    with open("tmp.txt", "w+") as f:
        f.write(tmp[1])
    os.system(command+ " tmp.txt > " +tmp[0]+".xml")
    print(tmp[0])
