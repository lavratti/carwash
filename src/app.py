import json
import dash
import dash_cytoscape as cyto
from dash import html

with open("temp/output_nodes.json", "r", encoding="utf-8") as fp:
    nodes = json.load(fp)
with open("temp/output_grafo.json", "r", encoding="utf-8") as fp:
    graph = json.load(fp)

my_elements = []
for i in range(len(nodes["name"])):
    my_elements.append(
        {
            "data": {"id": str(nodes["id"][i]), "label": str(nodes["name"][i])},
            #"classes": [nodes["type"][i], "node-w-{}".format(nodes["weight"][i]),]
        }
    )
for i in range(len(graph["from"])):
    my_elements.append(
        {
            "data": {"source": str(graph["from"][i]), "target": str(graph["to"][i])},
            #"classes": "edge-w-{}".format(graph["weight"][i]),
        }
    )


# cyto.load_extra_layouts()

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [
                "Grafo Operação Lava-jato.",
                html.Br(),
                "Dados obtidos do ",
                html.A(
                    "Site do Ministério Público Federal",
                    href="http://www.mpf.mp.br/grandes-casos/lava-jato/",
                ),
            ]
        ),
        cyto.Cytoscape(
            id="cytoscape",
            layout={"name": "cose"},
            elements=my_elements,

        ),
        html.Div(
            [
                "Autor Lucas L. (Repositório",
                html.A("Github", href="https://github.com/lavratti/carwash/"),
                ")",
                html.Br(),
                "Trabalho entregre referente a Disciplina de Construção de Interpretadores - 2022 / 1º",
                html.Br(),
                "Pontifícia Universidade Católica do Paraná",
                html.Br(),
            ]
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
