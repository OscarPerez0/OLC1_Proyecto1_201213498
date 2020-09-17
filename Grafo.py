import pydot
from PIL import Image

class Grafo:
    def __init__(self, ers):
        self.l_er = ers


    def generar_grafo(self):
        if len(self.l_er) < 1:
            return


        callgraph = pydot.Dot(graph_type='digraph')

        keys = list(self.l_er)
        for text in keys:
            if text == 'id':
                callgraph.add_subgraph(self.grafo_id())
            elif text == 'entero':
                callgraph.add_subgraph(self.grafo_numero())
            elif text == 'decimal':
                callgraph.add_subgraph(self.grafo_decimal())
            elif text == 'cadena':
                callgraph.add_subgraph(self.grafo_cadena())
            elif text == 'cadena_s':
                callgraph.add_subgraph(self.grafo_cadena_s())
            elif text == 'comentario_m':
                callgraph.add_subgraph(self.grafo_comentario_m())
            elif text == 'comentario_s':
                callgraph.add_subgraph(self.grafo_comentario_s())

        callgraph.write_raw('Reportes/automata.dot')
        callgraph.write_png('Reportes/automata.png')

        im = Image.open('Reportes/automata.png')
        im.show()

    def grafo_id(self):
        cluster_id = pydot.Cluster('id', label= 'Identificador')

        cluster_id.add_node(pydot.Node('S0', label='S0'))
        cluster_id.add_node(pydot.Node('S1', label='S1', color='green'))

        cluster_id.add_edge(pydot.Edge('S0', 'S1', label='L'))
        cluster_id.add_edge(pydot.Edge('S1', 'S1', label='L'))
        cluster_id.add_edge(pydot.Edge('S1', 'S1', label='N'))
        cluster_id.add_edge(pydot.Edge('S1', 'S1', label='_'))

        return cluster_id

    def grafo_numero(self):
        cluster_entero = pydot.Cluster('entero', label='Entero')

        cluster_entero.add_node(pydot.Node('B0', label='B0'))
        cluster_entero.add_node(pydot.Node('B1', label='B1', color='green')) #put color

        cluster_entero.add_edge(pydot.Edge('B0', 'B1', label='N'))
        cluster_entero.add_edge(pydot.Edge('B1', 'B1', label='N'))

        return cluster_entero

    def grafo_decimal(self):
        cluster_decimal = pydot.Cluster('decimal', label='Decimal')

        cluster_decimal.add_node(pydot.Node('C0', label='C0'))
        cluster_decimal.add_node(pydot.Node('C1', label='C1'))
        cluster_decimal.add_node(pydot.Node('C2', label='C2')) #punto
        cluster_decimal.add_node(pydot.Node('C3', label='C3', color='green'))

        cluster_decimal.add_edge(pydot.Edge('C0', 'C1', label='N'))
        cluster_decimal.add_edge(pydot.Edge('C1', 'C2', label='.'))
        cluster_decimal.add_edge(pydot.Edge('C2', 'C3', label='N'))
        cluster_decimal.add_edge(pydot.Edge('C3', 'C3', label='N'))

        return  cluster_decimal


    def grafo_cadena(self):
        print('cadena')
        cluster_cadena = pydot.Cluster('cadena', label='Cadena')

        cluster_cadena.add_node(pydot.Node('D0', label='D0'))
        cluster_cadena.add_node(pydot.Node('D1', label='D1'))
        cluster_cadena.add_node(pydot.Node('D2', label='D2', color='green'))

        cluster_cadena.add_edge(pydot.Edge('D0', 'D1', label='"'))
        cluster_cadena.add_edge(pydot.Edge('D1', 'D1', label='CC'))
        cluster_cadena.add_edge(pydot.Edge('D1', 'D2', label='"'))

        return cluster_cadena

    def grafo_cadena_s(self):
        print('cadena_s')
        cluster_cadena_s = pydot.Cluster('cadena_s', label='Cadena Simple')

        cluster_cadena_s.add_node(pydot.Node('E0', label='E0'))
        cluster_cadena_s.add_node(pydot.Node('E1', label='E1'))
        cluster_cadena_s.add_node(pydot.Node('E2', label='E2', color='green'))

        cluster_cadena_s.add_edge(pydot.Edge('E0', 'E1', label="'"))
        cluster_cadena_s.add_edge(pydot.Edge('E1', 'E1', label='CC'))
        cluster_cadena_s.add_edge(pydot.Edge('E1', 'E2', label="'"))

        return cluster_cadena_s

    def grafo_comentario_m(self):
        print('comentario_m')
        cluster_comment = pydot.Cluster('comentario_m', label='Comentario Multilinea')

        cluster_comment.add_node(pydot.Node('F0', label='F0'))
        cluster_comment.add_node(pydot.Node('F1', label='F1'))
        cluster_comment.add_node(pydot.Node('F2', label='F2'))
        cluster_comment.add_node(pydot.Node('F3', label='F3'))
        cluster_comment.add_node(pydot.Node('F4', label='F4', color='green'))

        cluster_comment.add_edge(pydot.Edge('F0', 'F1', label='/'))
        cluster_comment.add_edge(pydot.Edge('F1', 'F2', label='*'))
        cluster_comment.add_edge(pydot.Edge('F2', 'F2', label='CC'))
        cluster_comment.add_edge(pydot.Edge('F2', 'F3', label='*'))
        cluster_comment.add_edge(pydot.Edge('F3', 'F4', label='/'))

        return cluster_comment


    def grafo_comentario_s(self):
        print('comentario_s')
        cluster_comment = pydot.Cluster('comentario_s', label='Comentario Simple')

        cluster_comment.add_node(pydot.Node('G0', label='G0'))
        cluster_comment.add_node(pydot.Node('G1', label='G1'))
        cluster_comment.add_node(pydot.Node('G2', label='G2', color='green'))

        cluster_comment.add_edge(pydot.Edge('G0', 'G1', label='/'))
        cluster_comment.add_edge(pydot.Edge('G1', 'G2', label='/'))
        cluster_comment.add_edge(pydot.Edge('G2', 'G2', label='CC'))

        return cluster_comment


