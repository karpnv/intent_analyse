from intent_graph import Intent_graph
import igraph
import sys
sys.path.append('../gSpan')
from graph import *
from gspan import gSpan
import logging

def split_to_independent_subgraphs(igrs):
    k=0
    subgraphs={}
    for j in igrs:
        gr=igrs[j].copy()
        for tup in gr.get_edgelist():
            if tup[0]==0:
                gr.delete_edges(tup)
        edge_lists=gr.clusters(mode='WEAK')
        for edge_list in edge_lists:
            sgr=gr.subgraph(edge_list)
            if len(sgr.get_edgelist())!=0:
                subgraphs[k]=sgr
                k+=1
    return subgraphs

def read_gml_graphs(database_file_name, group_id=0, is_generalise=0, has_root=1):
    graphs = dict()
    ig=Intent_graph(database_file_name)
    igraphs=ig.iter_dir(igraph.Graph().Read_GML, '.gml', group_id)
    if has_root:
        min_support =len(igraphs) // 2
    else:
        igraphs=split_to_independent_subgraphs(igraphs)
        min_support =len(igraphs) // 40

    if is_generalise:
        igraphs=ig.generalise_letters(igraphs)
        attr_name='g_intent'
    else:
        min_support=min_support // 2
        attr_name='intent'

    tgraph, graph_cnt, edge_cnt = None, 0, 0
    for igr in igraphs:
        tgraph = Graph(graph_cnt, is_undirected = 0, eid_auto_increment = True)
        for j, type_j in enumerate(zip(igraphs[igr].vs[attr_name],igraphs[igr].vs['target'])):
            tgraph.add_vertex(j, type_j[0]+type_j[1])
        for edge in igraphs[igr].get_edgelist():
            tgraph.add_edge(AUTO_EDGE_ID, edge[0], edge[1], 1)
        graphs[graph_cnt] = tgraph
        graph_cnt += 1
        if tgraph != None: # adapt to input files that do not end with 't # -1'
            graphs[graph_cnt] = tgraph
    return graphs,min_support


def find_subgraph(group_id, is_generalise=0, has_root=1):
    graphs,min_support=read_gml_graphs('../with_tags',
                group_id=group_id,
                is_generalise=is_generalise,
                has_root=has_root)

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
    logging.info('Number of graphs = %s, min_support = %s, min_num_vertices = %s',len(gs.graphs), gs.min_support, gs.min_num_vertices)
    gs.run()
    gs.report_df.to_csv('gen/group'+str(group_id)+'_hubermas'+str(is_generalise)+'_root'+str(has_root)+'_supp'+str(gs.min_support)+'_min'+str(gs.min_num_vertices)+'.csv', sep=';', encoding='cp1251')

if __name__ == '__main__':
    for j in range(1,10):
        find_subgraph(group_id=j,
                      is_generalise=0,
                      has_root=1)
    print('ok')
