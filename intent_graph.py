import igraph as g
import pandas as pd
import os
import logging
class Intent_graph():
    def __init__(self):
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
        self.dir='with_tags'#'politru/-21337773_1/'

    def parse(self, f_name='comm_politru_2_23812.csv'):
        g1 = g.Graph()
        g1.add_vertices(1)
        df1=pd.read_csv(f_name, encoding='cp1251', sep=';', header=0)#cp1251#UTF-8
        #print(['']+df1.ix[:,-2].tolist())
        g1.add_vertices(df1.shape[0])
        g1.vs["name"]=['root']+df1['Id of comment.'].apply(str).tolist()
        g1.vs["author"]=['']+df1['Id of author of comment.'].apply(str).tolist()
        g1.vs["text"]=['']+df1['text'].tolist()
        g1.vs["likes"]=[0]+df1['likes'].tolist()
        g1.vs["date"]=[0]+df1['date'].tolist()
        g1.vs["intent"]=['']+df1.ix[:,-2].fillna('').tolist()
        g1.vs["content"]=[0]+df1.ix[:,-1].tolist()
        #print(g1.vs["intent"])
        #g1.vs["label"] = g1.vs["name"]
        for item in df1.iterrows():
            try:
                start,stop=item[1]['text'].find('[id'),item[1]['text'].find('|')
                if start>=0 and stop>=0:
                    #print(item[1]['text'][start+3:stop])
                    authors_messages=df1[
                        df1['Id of author of comment.']==int(item[1]['text'][start+3:stop])][
                        df1['Id of comment.']<item[1]['Id of comment.']][
                        'Id of comment.']
                    if authors_messages.shape[0]>0:
                        last_authors_message=authors_messages.values[-1]
                        g1.add_edge(str(last_authors_message),str(item[1]['Id of comment.']))
                    else:
                        #создать вершину и добавить ребро от нее
                        pass
                else:
                    #print(item[1])
                    g1.add_edge('root',str(item[1]['Id of comment.']))
            except AttributeError:
                #logging.info('Empty message in line \n %s', item[1])
                pass
        return g1

    def show(self, g1, fname):
        #print(fname, g1)
        layout = g1.layout("tree", root=[0])
        visual_style={}
        visual_style["layout"] = layout
        #visual_style["vertex_label"] = g1.vs["name"]
        #visual_style["vertex_label_dist"] = -4
        #visual_style["bbox"] = (300, 300)
        g.plot(g1, fname+'.pdf', **visual_style)
        #g.plot(self.g1, layout=layout)#, vertex_color = ["blue"]+["red"]*37)


    def iter_dir(self, func, ext_name='.csv'):
        graph_dict={}
        for name in sorted(os.listdir(self.dir)):
            path = os.path.join(self.dir, name)
            if os.path.isdir(path):
                for fname in sorted(os.listdir(path)):
                    if fname[-4:]==ext_name:
                        fpath = os.path.join(path, fname)
                        print(fpath)
                        g1=func(fpath)
                        graph_dict[fname[:-4]]=g1
        return graph_dict

    def write_gml(self, fpath):
        logging.info('%s', fpath)
        g1 = self.parse(fpath)
        g1.write_gml(fpath[:-4] + '.gml')
        # self.show(g1,fpath[:-4])
        return g1

    def read_gml(self, fpath):
        g1 = g.Graph()
        return g1.Read_GML(fpath)

    def take_path(self, graph):
        print(graph)

gr=Intent_graph()
#graph_dict=gr.iter_dir(gr.write_gml, '.csv')
graph_dict=gr.iter_dir(gr.read_gml, '.gml')
for key in graph_dict:
    gr.take_path(graph_dict[key])
