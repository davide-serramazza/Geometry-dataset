from color import color_list
from PIL import Image, ImageDraw
import random
from new_coordinate import new_cordinate,new_cordinate_circle
from lxml import etree

# create black background
im = Image.new('RGB', (1000, 1000), (0, 0, 0))
draw = ImageDraw.Draw(im)

# keep track of depth and breadth, current coordinates and a tree and a sentence as targets
current_depth = 0
current_degree = 1
x1 = 25
x2= 975
y1= 25
y2= 975
spaces = [(x1,y1,x2,y2)]

root = etree.Element("background", color="Black")
last_node = root

sentence="A Black background and"

next_level = True
while next_level:
    s=spaces.pop()
    print(s,spaces)
    x1=s[0]
    x2 =s[2]
    y1 = s[1]
    y2 = s[3]

    # select current shape and color
    shape = random.randint(0,1)
    choosed_color = random.randint(0,len(color_list)-1)
    color_name,rgb = color_list[choosed_color]

    if shape==0:
        # square
        #print(x1,x2,y1,x2)
        draw.rectangle([x1,y1,x2,y2],width=3,fill=rgb)
        x1,x2,y1,y2 = new_cordinate(x1,x2,y1,y2)
        child = etree.Element('child',color=color_name,shape='square')
        last_node.append(child)
        last_node=child
        sentence+=" a "+color_name+" square"
    else:
        # circle
        #print(x1,x2,y1,x2)
        draw.ellipse([x1,y1,x2,y2],width=3,fill=rgb)
        x1,x2,y1,y2 = new_cordinate_circle(x1,x2,y1,y2)
        child = etree.Element('child',color=color_name,shape='circle')
        last_node.append(child)
        last_node = child
        sentence+=" a "+color_name+" circle"

    next_level = x1<x2 and y1<y2
    if next_level:
        sentence+=" containing"
    spaces.append((x1,y1,x2,y2))
    current_depth+=1
    current_degree = random.randint(1,4)


tree_string = etree.tostring(root, pretty_print=True)
print((tree_string).decode('utf8'))
with open("tree.xml","w+") as f:
    f.write((tree_string).decode('utf8'))
print(sentence)
im.show()