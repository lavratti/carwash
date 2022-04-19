import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://transparencia.cc/dados/socios/nnnn/NOMENOME'

socio_primario = url.split('/')[-2].upper().replace('-', ' ')
# Busca a página web (precisa de User-Agent se não retorna 403)
page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
page = page.text
soup = BeautifulSoup(page, features="lxml")
caixas_ativas = soup.find_all("div", {"class": "caixa_ativa"})


socios = []
empresas = []
for caixa_ativa in caixas_ativas:
    caixa_ativa = "{}".format(caixa_ativa)
    ini_socio = caixa_ativa.find('<strong>') + len('<strong>')
    end_socio = caixa_ativa.find('</strong>', ini_socio)
    if not "<" in caixa_ativa[ini_socio:end_socio]:
        socios.append(caixa_ativa[ini_socio:end_socio])
        ini_empresa = caixa_ativa.find('na empresa <strong>') + len('na empresa <strong>')
        end_empresa = caixa_ativa.find('</strong>', ini_empresa)
        empresas.append(caixa_ativa[ini_empresa:end_empresa])
        socios.append(socio_primario)
        empresas.append(caixa_ativa[ini_empresa:end_empresa])

# Dump em csv
with open('output.csv', 'w') as fp:
    fp.write('"SOCIO", "EMPREENDIMENTO\n')
    for i in range(len(socios)):
        fp.write('"{}", "{}\n'.format(socios[i], empresas[i]))


# Plot Graph
relationships = pd.DataFrame({ 'from':socios, 'to':empresas})
carac = {'ID':[], 'type':[]}
for s in socios:
    if not s in carac['ID']:
        carac['ID'].append(s)
        carac['type'].append('socio')
for e in empresas:
    if not e in carac['ID']:
        carac['ID'].append(e)
        carac['type'].append('empresa')
carac = pd.DataFrame(carac)
G = nx.from_pandas_edgelist(relationships, 'from', 'to', create_using=nx.Graph())
carac=carac.set_index('ID')
carac=carac.reindex(G.nodes())
carac['type']=pd.Categorical(carac['type'])
carac['type'].cat.codes
cmap = matplotlib.colors.ListedColormap(['dodgerblue', 'lightgray', 'darkorange'])
node_sizes = [100 if entry != 'empresa' else 400 for entry in carac.type]

plt.title('Grafo de sócios e empreendimentos realcionados', fontsize=10)
nx.draw(G, with_labels=True, node_color=carac['type'].cat.codes, cmap=cmap, 
        node_size = node_sizes, edgecolors='gray')
plt.show()
