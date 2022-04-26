import json
import urllib.request


url_mpf = 'http://www.mpf.mp.br/grandes-casos/lava-jato/acoes/lavajato-acoes-view'
raw_html = urllib.request.urlopen(url_mpf).read().decode("utf8")

envolvidos_por_acao = []
lines = raw_html.splitlines()

for i in range(len(lines)):

    """
        if '                                    <p>' in lines[i]:
            acao['data'] = str(lines[i][39:49]) #datetime.strptime(str(lines[i][39:49]), '%d/%m/%Y')

        if '                                        <b>'in lines[i]:
            acao['acao'] = lines[i][43:-5]

        if '                                    <h4>' in lines[i] and lines[i][40].isalnum():
            acao['numero'] = lines[i][40:-6]
            acao['numero'] = acao['numero'][:acao['numero'].find(' ')]
    """
    if 'ENVOLVIDOS' in lines[i]:
        j = 1
        envolvidos = lines[i+j][42:]
        while not '</div>' in lines[i+j]:
            j += 1
            envolvidos += lines[i+j]
        envolvidos = envolvidos.replace(' e', ', ')
        envolvidos = envolvidos.replace(' e ', ', ')
        envolvidos = envolvidos.replace('\n', '')
        envolvidos = envolvidos.replace('&nbsp', ' ')
        envolvidos = envolvidos.replace(';', ' ')
        envolvidos = envolvidos.replace('.', ' ')
        envolvidos = envolvidos.replace('<div>', ' ')
        envolvidos = envolvidos.replace('</div>', ' ')
        while '  ' in envolvidos: 
            envolvidos = envolvidos.replace('  ', ' ')
        envolvidos = envolvidos.strip()
        envolvidos = list(set(envolvidos.split(sep=', ')))
        envolvidos = [x for x in envolvidos if len(x) < 100 and x[0].isupper()]

    if 'clearfix' in lines[i]:
        envolvidos_por_acao.append(envolvidos)

unique_envolvidos = []
for grupo in envolvidos_por_acao:
    for pessoa in grupo:
        if not pessoa in unique_envolvidos:
            unique_envolvidos.append(pessoa)

acoes_por_pessoa = {}
for acao in envolvidos_por_acao:
    for envolvido in acao:
        acoes_por_pessoa[envolvido] = 0
for acao in envolvidos_por_acao:
    for envolvido in acao:
        acoes_por_pessoa[envolvido] += 1
dict_pesos = {
    'nome' : [],
    'casos': []
}
for envolvido in acoes_por_pessoa.keys():
    dict_pesos['nome'].append(envolvido)
    dict_pesos['casos'].append(acoes_por_pessoa[envolvido])

dict_grafo = {
                'to': [],
                'from': []
            }

for acao in envolvidos_por_acao:
    for envolvido in acao:
        for outro_envolvido in acao:
            if not envolvido == outro_envolvido:
                dict_grafo['to'].append(envolvido)
                dict_grafo['from'].append(outro_envolvido)


vis_nodes = []
i = 0
for pessoa in unique_envolvidos:
    i += 1
    vis_nodes.append({"id":i, "value":acoes_por_pessoa[pessoa], "label":pessoa})

vis_edges = []
for acao in envolvidos_por_acao:
    for envolvido in acao:
        for outro_envolvido in acao:
            if not envolvido == outro_envolvido:
                vis_edges.append({'from':envolvido, 'to':outro_envolvido, 'value':1})


with open('temp/json_out_nodes.json', 'w') as fp:
    json.dump(vis_nodes, fp)
with open('temp/json_out_edges.json', 'w') as fp:
    json.dump(vis_edges, fp)

"""
# libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
 
# Build a dataframe with your connections
df = pd.DataFrame(dict_grafo)
 
# And a data frame with characteristics for your nodes
carac = pd.DataFrame(dict_pesos)
 
# Build your graph
G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph() )
 
# The order of the node for networkX is the following order:
G.nodes()
# NodeView(('A', 'D', 'B', 'C', 'E'))

# Thus, we cannot give directly the 'myvalue' column to netowrkX, we need to arrange the order!
 
# Here is the tricky part: I need to reorder carac, to assign the good color to each node
carac= carac.set_index('nome')
carac=carac.reindex(G.nodes())
 
# Plot it, providing a continuous color scale with cmap:
nx.draw(G, with_labels=False, node_color=carac['casos'].astype(int), cmap=plt.cm.hot)
plt.show()
"""