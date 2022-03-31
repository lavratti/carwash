import os
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from tqdm import tqdm
from names import pt_names

def show_graph_with_labels(mymatrix, mylabels):
    rows, cols = np.where(mymatrix > 0)
    w = []
    for r, c in zip(rows, cols):
        w.append(mymatrix[r][c])

    edges = zip(rows.tolist(), cols.tolist(), w)
    gr = nx.Graph()
    gr.add_weighted_edges_from(edges)
    nx.draw(gr, node_size=500, labels=mylabels, with_labels=True,  width=w)
    plt.show()

pt_names = sorted(pt_names)
name_keys = {}
i = 0
for name in pt_names:
    name_keys[name] = i
    i += 1

name_matrix = []
for name in pt_names:
    temp = [ ]
    for other_name in pt_names:
        temp.append(0)
    name_matrix.append(temp)


texts = []

pardir = os.path.join(os.path.dirname(__file__), "..", "books")
txt_paths = [os.path.join(os.path.dirname(__file__), "..", "books", f) for f in os.listdir(pardir) if os.path.isfile(os.path.join(pardir, f)) and f[-4:] == ".txt"]
txt_paths = sorted(txt_paths)

for fpath in tqdm(txt_paths[:5]):
    text = {"txt_path": fpath }
    with open(fpath, "rb") as text_file:
        lines = [ l.decode('latin1') for l in text_file.readlines()]
        lines = " ".join(lines)
        lines = lines.split("\r\n")
        paras = []
        para = ""
        for line in lines:
            if line == "\n" or line == "\r\n" or line == "" or line == " ":
                if len(para) > 5:
                    paras.append(para)
                para = ""
            else:
                para = "{} {}".format(para, line)
        text["paras"] = paras
    texts.append(text)

for text in tqdm(texts):
    for paragraph in text["paras"]:
        names_in_para = []
        for name in pt_names:
            if " " + name + " " in paragraph:
                names_in_para.append(name)
        for name in names_in_para:
            for other_name in names_in_para:
                if name != other_name:
                    name_matrix[name_keys[name]][name_keys[other_name]] += 1
                    #print(name, "-", other_name,"->", name_matrix[name_keys[name]][name_keys[other_name]] )

am = np.array(name_matrix)
#print(am)
show_graph_with_labels(am, pt_names)