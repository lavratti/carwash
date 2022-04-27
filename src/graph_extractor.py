import logging
import re
import traceback
import urllib.request
from os import path

# Inicialização do módulo para log
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
ch = logging.StreamHandler()
fh = logging.FileHandler("temp/carwash.log")
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)
logger.info("Iniciando Script")

# Página do Ministério Público Federal
url = "http://www.mpf.mp.br/grandes-casos/lava-jato/acoes/lavajato-acoes-view"

# Se existe uma cópia local da página, usar ela, senão request.
if path.isfile("temp/cashed_response.html"):
    logger.info("Cópia local da página encontrada.")
    with open("temp/cashed_response.html", "r") as fp:
        raw_html = fp.read()

else:
    # Faz a request da página do Ministério Público Federal e salva localmente.
    logger.info("Baixando cópia da página.")
    try:
        response = urllib.request.urlopen(url)
        raw_html = response.read().decode("utf8")
        with open("temp/cashed_response.html", "w") as fp:
            fp.write(raw_html)

    # Se a request falhar, escrever o motivo no log.
    except Exception as e:
        logger.error("A requisição da url falhou.")
        logger.debug(traceback.format_exc())


# Com o documento em memória, varrer para encontrar os envolvidos e colocar em uma lista.
logger.info("Varrendo arquivo...")
envolvidos_por_acao = []
inicio_bloco = 0
final_bloco = 0
pos_atual = 0
while pos_atual < len(raw_html):

    # Encontra o proximo "token" 'ENVOLVIDOS'
    pos_atual = raw_html.find("ENVOLVIDOS", final_bloco)
    inicio_bloco = raw_html.find("<div>", pos_atual) + len("<div>")
    final_bloco = raw_html.find("</div>", inicio_bloco)
    bloco = raw_html[inicio_bloco:final_bloco]

    # Se não encontrar, sai do loop
    if pos_atual == -1 or inicio_bloco == -1 or final_bloco == -1 or len(bloco) < 1:
        break

    # Tratamento do bloco encontrado a lista de blocos
    # Troca " e" por ", "
    # Troca ";", ".", "\n" e outros caracteres de espaço, como "&nbsp" por " "
    # Remove espaços repetidos, à esquerda e à direita
    # Separa a string (todos os envolvidos) em uma lista de strings (cada envolvido)
    # Remove da lista de envolvidos alguns valores estranhos
    bloco = re.sub("[ ][e]", ", ", bloco)
    bloco = re.sub("[;.\n\s]", " ", bloco)
    bloco = re.sub(" +", " ", bloco)
    bloco = bloco.strip()
    bloco = list(set(bloco.split(sep=", ")))
    bloco = [x for x in bloco if len(x) < 100 and x[0].isupper()]

    # Adciona para a lista de envolvidos agrupados por ação
    envolvidos_por_acao.append(bloco)

logger.info("Processando blocos de açõe/envolvidos...")

# Buscar cada um dos envolvidos, sem repetir, e colocar em uma lista
unique_envolvidos = []
for grupo in envolvidos_por_acao:
    for pessoa in grupo:
        if not pessoa in unique_envolvidos:
            unique_envolvidos.append(pessoa)

# Montar dicionário de pesos baseado no número de ações de cada envolvido
# Inicializar o dicionário de # ações por pessoa
acoes_por_pessoa = {}
for envolvido in unique_envolvidos:
    acoes_por_pessoa[envolvido] = 0
# Contar em quantas ações cada envolvido participou
for acao in envolvidos_por_acao:
    for envolvido in acao:
        acoes_por_pessoa[envolvido] += 1


################################################################################
# Montar dicionários do grafo
################################################################################


# Montar dicionário com os nós do grafo
dict_nodes = {
    "name": [],
    "type": [],
    "weight": [],
}
# Append Envolvidos
for envolvido in acoes_por_pessoa.keys():
    dict_nodes["name"].append(envolvido)
    dict_nodes["type"].append("envolvido")
    dict_nodes["weight"].append(acoes_por_pessoa[envolvido])
# Append Ações
id = 0
for grupo in envolvidos_por_acao:
    dict_nodes["name"].append("acao-".format(id))
    dict_nodes["type"].append("acao")
    dict_nodes["weight"].append(len(grupo))
    id += 1

# Montar dicionário com as ligações do grafo
id = 0
dict_grafo = {"to": [], "from": [], "weight": []}
for grupo in envolvidos_por_acao:
    for envolvido in grupo:
        dict_grafo["to"].append("acao-".format(id))
        dict_grafo["from"].append(envolvido)
        dict_grafo["weight"].append((acoes_por_pessoa[envolvido] + len(grupo)) / 2)
    id += 1

logger.info("Total de ações: {}".format(len(envolvidos_por_acao)))
logger.info("Total de envolvidos: {}".format(len(unique_envolvidos)))
logger.info("Total de relações: {}".format(len(dict_grafo["to"])))
