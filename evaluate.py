import json

def take_sen(f_name):
    f = open(f_name)
    sens = f.readlines()
    d = {}
    for el in sens:
        d[el[:8]] = el[11:]
    return d

def analyze_first_level(first_level_first, first_level_second, matched, tot):
    first_figs = first_level_first.split("and")
    for fig in first_figs:
        tot += 1
        # replace leading "a ...." or " a .... "
        if fig.startswith("a "):
            fig = fig[2:]
        if fig.startswith(" a "):
            fig = fig[3:]
        if fig.replace(" \n", "").replace("and", "") in first_level_second:
            if (fig.count("square") > 0 or fig.count("circle") > 0):
                matched += 1
    return matched, tot

def analyze_second_third_level(first, second, matched, tot):
    # dictionary of level
    d_level = {'the first one containing': 0,'the second one containing':1,
               'the third one containing' :2,'the fourth one containing':3 }
    to_del = list(d_level.keys())
    first_figs = first.split(";")
    if first.count(" in turn ")>0:
        a=2
    for breadth in first_figs:
        # for each branch of the tree
        figs = breadth.split("and")
        # for each leaf
        if figs!=['\n']:
            for fig in figs:
                if fig.count("square")>0 or fig.count("circle")>0:
                    # if and only if is really the description of a figure
                    tot+=1
                    # remove the not necessary strings
                    for el in to_del:
                        fig = fig.replace(el,"")
                    if len(fig.split(" in "))>1:
                        fig=fig.split(" in ")[0]
                    # TODO creare una funzione nella quale vvado a rimuovere tutte le possibile altre cose (Aggiungere anche "\n ed "  \n")
                    if fig.startswith("  a"):
                        fig=fig[4:]
                    if fig.startswith(" a"):
                        fig=fig[3:]
                    if fig.startswith("a"):
                        fig=fig[2:]
                    if fig.replace(" \n", "").replace("and", "") in second:
                        matched+=1
                    print(fig.replace(" \n", ""))

    return matched, tot

def first_in_second(first_d,second_d):
    tot_first = 0
    matched_first = 0
    tot_second = 0
    matched_second = 0
    imgs = list( first_d.keys())
    for el in imgs:
        first_level_first = first_d[el].split(" : ")[0]
        first_level_second = second_d[el].split(" : ")[0]
        matched_first, tot_first = analyze_first_level(first_level_first, first_level_second, matched_first, tot_first)
        if len (first_d[el].split(" : ") )>1:
            second_level_first = first_d[el].split(" : ")[1]
            try:
                second_level_second = second_d[el].split(" : ")[1]
            except IndexError:
                second_level_second =""
            a=2
            matched_second,tot_second=analyze_second_third_level(second_level_first, second_level_second, matched_second, tot_second)
    print("first level ",tot_first,matched_first/tot_first)
    print("second level ",tot_second,matched_second/tot_second)

file_n="emb_dim_500_rnn_units_300_beta_0.0_hidden_coeff_4_lambd_8_drop_rate_0.2_it=60_beam=True.txt"
preds_d = take_sen("/home/davide/valentia_galli/"+file_n)
refs = take_sen("/home/davide/valentia_galli/my_dataset_sentences2.txt")
refs_d = {}
for el in preds_d.keys():
    refs_d[el] = refs[el]
print(len(preds_d),len(refs_d))

first_in_second(preds_d,refs_d)
#first_in_second(refs_d,preds_d)













"""
def first_in_second(d1,split_d1,d2,split_d2):
    tot = 0
    matched = 0
    for el in d1:
        d1_first_level = d1[el].split(split_d1)[0]
        d1_figs = d1_first_level.split(" a ")
        #d1_figs[0]=d1_figs[0].replace("a","")
        d2_first_level = (d2[el].split(split_d2)[0]).replace("\n","")
        for el in d1_figs:
            tot+=1
            if el.startswith("a "):
                el = el[2:]
            if el.replace("and","").replace("\n","") in d2_first_level:
                matched+=1
    print(tot,matched,matched/tot)



def second_level(d1,d2):
    matched=0
    tot=0
    for el in d1:
        if d1[el] =="":
            a = 2
        level2 = d1[el].split("the")[1:]
        for level in level2:
            for fig in level.split("and"):
                fig = fig.split(" containing ")
                tot+=1
                if fig[-1].replace("\n","").replace(" ;","") in d2[el]:
                    matched+=1
    print(tot,matched,matched/tot)

file_n="emb_dim_500_rnn_units_300_beta_0.0_hidden_coeff_4_lambd_8_drop_rate_0.2_it=30_beam=False.txt"
preds_d = take_sen("/home/davide/valentia_galli/"+file_n)
refs = take_sen("/home/davide/valentia_galli/my_dataset_sentences2.txt")
print(len(preds_d),len(refs))

refs_d = {}
for el in preds_d.keys():
    refs_d[el] = refs[el]

print(len(refs_d))
first_in_second(preds_d,":",refs_d,":")
first_in_second(refs_d,":",preds_d,":")

refs_d2 = {}
for el in refs_d:
    try:
        refs_d2[el] = refs_d[el].split(" : ")[1].replace("\n","")
    except IndexError:
        continue
preds_d2 = {}
for el in preds_d:
    try:
        preds_d2[el] = preds_d[el].split(" : ")[1]
        a = 2
    except IndexError:
        preds_d2[el] = ""

second_level(preds_d2,refs_d2)
second_level(refs_d2,preds_d2)



def second_level(d1,d2):
	matched=0
	tot=0
	for el in d1:
		level2 = d1[el].split("the")
		for ell in level2:
			figs = ell.split(" and ")
			for fig in figs:
				tot+=1
				if fig.replace(" ;","") in d2[el] and fig!="":
					matched+=1
					print(fig.replace(" ;",""))
	print(tot,matched)
"""