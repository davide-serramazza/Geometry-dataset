import math

def new_cordinate_circle(x1, x2, y1, y2):
    center = (x2 + x1) / 2
    radius = (x2-x1) /2
    sin_cos = radius * math.sqrt(2) / 2
    x1 = center - sin_cos
    x2 = center + sin_cos
    y1 = center - sin_cos
    y2 = center + sin_cos

    #print(s, x1, x2, y1, y2)
    return x1, x2, y1, y2

def new_cordinate(x1,x2,y1,y2):
    return  x1+50, x2-50,y1+50,y2-50