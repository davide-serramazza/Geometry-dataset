import os
import subprocess
from tqdm import tqdm
import sys


current_dir = os.getcwd()
exit()
new_dir = "/home/davide/stanford_parser/"
os.chdir(new_dir)
command = "java -mx2000m -cp ./*: edu.stanford.nlp.parser.lexparser.LexicalizedParser -sentences newline -outputFormat xmlTree edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz "
part = "1"
s = part+".txt" #sys.argv[1]
print(command+s)

subprocess = subprocess.Popen(command+current_dir+"/"+s+" > "+current_dir+"/"+s+"_parsed", shell=True, stdout=subprocess.PIPE)
subprocess_return = subprocess.stdout.read()
print(len(subprocess_return),(subprocess_return))





"""
# dizionariIIII con caption
import json
f = open("/home/davide/Desktop/my_dataset_sentences.txt")
lines = f.readlines()
d = {}
for el in lines:
    d[el[:9]] =[ el[12:-1] ]
with open("/home/davide/Desktop/all_captions.json","w+") as f:
    json.dump(d,f)
for el in lines:
    d[el[:9]].append( el[12:-1].replace("square","<unk>").replace("circle","<unk>")  )
with open("/home/davide/Desktop/all_captions2.json","w+") as f:
    json.dump(d,f)
"""



"""
split caption e nome pre stanford parser
    f = open("/home/davide/Desktop/my_dataset_sentences.txt")
    lines = f.readlines()
    fc = open("/home/davide/Desktop/caps.txt","w+")
    fn = open("/home/davide/Desktop/names.txt","w+")
    for el in lines:
        fn.write(el[:8]+"\n")
        fc.write( el[11:])
    fc.flush()
    fn.flush()
        """

"""""
#ricavare file xmls da txt unico ottenuto con stanforfdparser
current_s=""
fp = open("parsed_caps.txt")
fn = open("names.txt")
plines = fp.readlines()
names = fn.readlines()
names = ["fake\n"]+names
i=0
for el in plines:
    if el=='<node value="ROOT">\n':
        with open("xmls/"+names[i][:-1]+".xml","w+") as f:
            f.write(current_s)
        current_s=el
        i+=1
    else:
        current_s+=el
#final caption
with open("xmls/"+names[i][:-1]+".xml","w+") as f:
    f.write(current_s)
		
		
		
#dividere in più file per processing parallelo
f = open("/home/davide/Desktop/my_dataset_sentences.txt")
lines = f.readlines()
for part in [1,2,3,4]:
    imgs =  []
    sens =  []
    for i in range((part-1)*7500,part*7500):
        tmp = lines[i]
        imgs.append(tmp[:8])
        sens.append(tmp[11:])

    f = open(str(part)+".txt","w+")
    for el in sens:
        f.write(el)

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
