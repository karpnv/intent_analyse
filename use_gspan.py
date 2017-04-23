from intent_graph import Intent_graph
import igraph
import sys
sys.path.append('../gSpan')
from graph import Graph
AUTO_EDGE_ID = -1

def read_gml_graphs(database_file_name, group_id=0):
    graphs = dict()
    ig=Intent_graph(database_file_name)
    igraphs=ig.iter_dir(igraph.Graph().Read_GML, '.gml', group_id)
    min_support = len(igraphs) #// 2
    igraphs=ig.generalise_letters(igraphs)
    tgraph, graph_cnt, edge_cnt = None, 0, 0
    for igr in igraphs:
        tgraph = Graph(graph_cnt, is_undirected = 1, eid_auto_increment = True)
        #print(igr)
        for j, type_j in enumerate(zip(igraphs[igr].vs['g_intent'],igraphs[igr].vs['target'])):
            tgraph.add_vertex(j, type_j[0]+type_j[1])
        for edge in igraphs[igr].get_edgelist():
            tgraph.add_edge(AUTO_EDGE_ID, edge[0], edge[1], 1)
        graphs[graph_cnt] = tgraph
        graph_cnt += 1
        if tgraph != None: # adapt to input files that do not end with 't # -1'
            graphs[graph_cnt] = tgraph
    return graphs

print('ok')