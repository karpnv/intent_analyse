from intent_graph import Intent_graph
import igraph
import sys
sys.path.append('../gSpan')
from graph import *
from gspan import gSpan

def split_to_subgraphs(igraphs):
    k=0
    subgraphs={}
    for j in igraphs:
        for tup in igraphs[j].get_edgelist():
            if tup[0]==0:
                igraphs[j].delete_edges(tup)
        edge_lists=igraphs[j].clusters(mode='WEAK')
        for edge_list in edge_lists:
            subgraphs[k]=igraphs[j].subgraph(edge_list)
            k+=1
    return subgraphs

def read_gml_graphs(database_file_name, group_id=0):
    graphs = dict()
    ig=Intent_graph(database_file_name)
    igraphs=ig.iter_dir(igraph.Graph().Read_GML, '.gml', group_id)
    igraphs=split_to_subgraphs(igraphs)
    print(len(igraphs))
    min_support = len(igraphs) // 100
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
    return graphs,min_support

# GraphBase.decompose(mode=STRONG, maxcompno=None, minelements=1)
# independent_vertex_sets(min=0, max=0)
# induced_subgraph(vertices, implementation="auto")

def find_subgraph(group_id):
    graphs,min_support=read_gml_graphs('../with_tags',group_id=group_id)

    gs = gSpan(
        database_file_name='../gSpan/graphdata/graph.data.5',
        min_support=min_support,
        min_num_vertices=2,
        max_num_vertices=float('inf'),
        max_ngraphs=float('inf'),
        is_undirected=0,
        verbose=0,
        visualize=0,
        where=0)
    gs.graphs=graphs
    gs.run()
    gs.report_df.to_csv('gen/group'+str(group_id)+'_s'+str(gs.min_support)+'_l'+str(gs.min_num_vertices)+'.csv', sep=';')

if __name__ == '__main__':
    # for j in range(1,10):
    #     find_subgraph(j)
    find_subgraph(1)
    print('ok')
