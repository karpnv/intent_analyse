import igraph as g
import pandas as pd
import os
import logging
class Intent_graph():
    def __init__(self):
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
        self.dir='with_tags'#'politru/-21337773_1/'

    def parse(self, f_name='comm_politru_2_23812.csv'):
        self.g1 = g.Graph()
        self.g1.add_vertices(1)
        df1=pd.read_csv(f_name, encoding='cp1251', sep=';', header=0)#cp1251#UTF-8
        #print(['']+df1.ix[:,-2].tolist())
        self.g1.add_vertices(df1.shape[0])
        self.g1.vs["name"]=['root']+df1['Id of comment.'].apply(str).tolist()
        self.g1.vs["author"]=['']+df1['Id of author of comment.'].apply(str).tolist()
        self.g1.vs["text"]=['']+df1['text'].tolist()
        self.g1.vs["likes"]=[0]+df1['likes'].tolist()
        self.g1.vs["date"]=[0]+df1['date'].tolist()
        self.g1.vs["intent"]=['']+df1.ix[:,-2].fillna('').tolist()
        self.g1.vs["content"]=[0]+df1.ix[:,-1].tolist()
        print(self.g1.vs["intent"])
        #self.g1.vs["label"] = self.g1.vs["name"]
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
                        self.g1.add_edge(str(last_authors_message),str(item[1]['Id of comment.']))
                    else:
                        #создать вершину и добавить ребро от нее
                        pass
                else:
                    #print(item[1])
                    self.g1.add_edge('root',str(item[1]['Id of comment.']))
            except AttributeError:
                logging.info('Empty message in line \n %s', item[1])

        return self.g1

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

    def read_dir(self):
        for name in sorted(os.listdir(self.dir)):
            path = os.path.join(self.dir, name)
            if os.path.isdir(path):
                for fname in sorted(os.listdir(path)):
                    if fname[-4:]=='.csv':
                        fpath = os.path.join(path, fname)
                        logging.info('%s', fpath)
                        g1=self.parse(fpath)
                        g1.write_gml(fpath[:-4]+'.gml')
                        self.show(g1,fpath[:-4])

        # logging.info('%s', fpath)
        # g1=self.parse(fpath)
        # g1.write_gml(fpath[:-4]+'.gml')
        # self.show(g1,fpath[:-4])

gr=Intent_graph()
gr.read_dir()
