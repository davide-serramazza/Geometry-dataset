import sys


f = open(sys.argv[1])
lines = f.readlines()

print(len(lines), lines[0])

i=0
current_fig_n=0
current_fig_lines=[]
current_level= sys.argv[2]
while i<len(lines):
	current_fig_lines.append(lines[i])
	if lines[i]=='</node>\n':
		with open("xmls/"+str(current_level).zfill(3)+"_"+str(current_fig_n).zfill(4)+".xml", "w+") as xml:
			for el in current_fig_lines:
				xml.write(el)
			current_fig_lines=[]
			current_fig_n+=1
	i+=1
print(current_fig_n)

