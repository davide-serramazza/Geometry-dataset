import os
import subprocess
from tqdm import tqdm



new_dir = "/home/davide/stanford_parser/"
os.chdir(new_dir)
command = "java -mx500m -cp ./*: edu.stanford.nlp.parser.lexparser.LexicalizedParser -outputFormat xmlTree edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz "


subprocess = subprocess.Popen(command+s+"> senza_punt2.txt", shell=True, stdout=subprocess.PIPE)
subprocess_return = subprocess.stdout.read()
print(len(subprocess_return),(subprocess_return))







"""""
# estrai gli xml dal txt unico
with open("/home/davide/stanford_parser/sens_punt.txt", "r") as f:
    lines = f.readlines()
    f.close()

with open("my_dataset_sentences.txt", "r") as f:
    sens = f.readlines()
    f.close()

i=0
curr_item=0
s=""
first=True
while i<len(lines):
    if lines[i]=='<node value="ROOT">\n':
        if first:
            first=False
            s+=lines[i]
        else:
            name = sens[curr_item].split(" : ")[0]
            with open("punt_xml/"+name+".xml", "w+") as f:
                f.write(s)
            s=lines[i]
            curr_item+=1
            if curr_item%1000==0:
                print(curr_item)
    else:
        s+=lines[i]
    i+=1

with open("punt_xml/"+sens[-1].split(" : ")[0]+".xml", "w+") as f:
    f.write(s)
exit()



# con punto e tutti in unico file
with open("my_dataset_sentences.txt", "r") as f:
    sentences = f.readlines()

with open("temp.txt","w+") as f:
    for el in tqdm(sentences):
        tmp = el.split(" : ")
        f.write(tmp[1][:-1]+".\n")
    f.close()





#senza punto e un file per sentence
with open("my_dataset_sentences.txt", "r") as f:
    sentences = f.readlines()

for el in sentences:
    tmp = el.split(" : ")
    with open("sens/"+tmp[0],"w+") as f:
        f.write(tmp[1])



#raccogli tutti i file name
files = os.listdir("sens")
files.sort()
s =""
i=0
for el in  files:
    if i<6000:
        i+=1
        continue
    else:
        s+="sens/"+el+" "
        i+=1




#vecchio
for el in sentences:
    tmp = el.split(" : ")
    with open("tmp.txt", "w+") as f:
        f.write(tmp[1])
    os.system(command+ " tmp.txt > " +tmp[0]+".xml")
    print(tmp[0])
"""