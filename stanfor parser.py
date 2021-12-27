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







"""""
#ricavare file xmls da txt unico ottenuto con stanforfdparser
caps = []
current_s=""
fp = open("caps_parsed.txt")
plines = fp.readlines()
current_n=-1
for el in plines:
	if el=='<node value="ROOT">\n':
		with open("xmls/001_"+str(current_n).zfill(5)+".xml","w+") as f:
			f.write(current_s)
		current_s=el
		current_n+=1
	else:
		current_s+=el
		
		
		
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
