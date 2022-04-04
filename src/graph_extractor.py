from datetime import datetime
import json

nodes = []
node = {
    'acao': '',
    'data': '',
    'numero': '',
    'envolvidos': ''
}  

with open('MPF-Lava-jato.html', 'r') as raw_html:
    lines = raw_html.readlines()

for i in range(len(lines)):

    if '                                    <p>' in lines[i]:
        node['data'] = str(lines[i][39:49]) #datetime.strptime(str(lines[i][39:49]), '%d/%m/%Y')

    if '                                        <b>'in lines[i]:
        node['acao'] = lines[i][43:-5]

    if '                                    <h4>' in lines[i] and lines[i][40].isalnum():
        node['numero'] = lines[i][40:-6]

    if 'ENVOLVIDOS' in lines[i]:
        j = 1
        envolvidos = lines[i+j][42:]
        while not '</div>' in lines[i+j]:
            j += 1
            envolvidos += lines[i+j]
        envolvidos = envolvidos.replace(' e ', ', ')
        envolvidos = envolvidos.replace('\n', '')
        envolvidos = envolvidos.replace('.', ' ')
        envolvidos = envolvidos.replace('<div>', ' ')
        envolvidos = envolvidos.replace('</div>', ' ')
        while '  ' in envolvidos: 
            envolvidos = envolvidos.replace('  ', ' ')
        envolvidos = envolvidos.strip()

        node['envolvidos'] = list(set(envolvidos.split(sep=', ')))
    
    if 'clearfix' in lines[i]:
        nodes.append(node)
        node = {
        'acao': '',
        'data': '',
        'numero': '',
        'envolvidos': ''
        }  

with open('output.json', 'w') as outputfile:
    json.dump(nodes, outputfile)