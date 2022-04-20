from enum import unique
import json
from multiprocessing.sharedctypes import Value

grupos_de_envolvidos = []

with open('MPF-Lava-jato.html', 'r') as raw_html:
    lines = raw_html.readlines()

for i in range(len(lines)):

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
        grupos_de_envolvidos.append(envolvidos)

id = 0
ids_envolvidos = {}
pesos_envolvidos = {}

for grupo in grupos_de_envolvidos:
    for envolvido in grupo:
        if not envolvido in ids_envolvidos.keys():
            id += 1
            ids_envolvidos[envolvido] = id
            pesos_envolvidos[envolvido] = 0

for grupo in grupos_de_envolvidos:
    for envolvido in grupo:
        pesos_envolvidos[envolvido] += 1

pares_envolvidos = []

for grupo in grupos_de_envolvidos:
    for envolvido in grupo:
        for outro_envolvido in grupo:
            if (not envolvido == outro_envolvido 
                and sorted([envolvido, outro_envolvido]) not in pares_envolvidos):
                pares_envolvidos.append(sorted([envolvido, outro_envolvido]))

# VIS
limite_inferior = 0
vis_nodes = []
vis_edges = []

for envolvido in ids_envolvidos.keys():
    if pesos_envolvidos[envolvido] > limite_inferior:
        vis_nodes.append({"id":ids_envolvidos[envolvido], "value":pesos_envolvidos[envolvido], "label":envolvido})

for par in pares_envolvidos:
    if (pesos_envolvidos[par[0]] > limite_inferior
        and pesos_envolvidos[par[1]] > limite_inferior):
        vis_edges.append(
            {
                'from':ids_envolvidos[par[0]],
                'to':ids_envolvidos[par[1]],
                'value':min(pesos_envolvidos[par[0]],pesos_envolvidos[par[1]])
            }
        )


with open('json_out_nodes.json', 'w', encoding='utf8') as fp:
    json.dump(vis_nodes, fp, ensure_ascii=False,)
with open('json_out_edges.json', 'w', encoding='utf8') as fp:
    json.dump(vis_edges, fp, ensure_ascii=False,)
