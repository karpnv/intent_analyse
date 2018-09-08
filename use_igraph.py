import igraph


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

if __name__ == '__main__':
    print('asdfgh')
    # gr = igraph.Graph()
    # igraphs = .Read_GML, '.gml', group_id)