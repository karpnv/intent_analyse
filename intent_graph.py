import igraph as g
import pandas as pd
import os
class Intent_graph():
    def __init__(self):
        self.g1 = g.Graph()
        self.g1.add_vertices(1)
        self.dir='politru/-21337773_1/'

    def parse(self, f_name='comm_politru_2_23812.csv'):
        df1=pd.read_csv(self.dir+f_name, encoding='cp1251', sep=';', header=0)
        print(df1)
        self.g1.add_vertices(df1.shape[0])
        self.g1.vs["name"]=['root']+df1['Id of comment.'].apply(str).tolist()
        self.g1.vs["author"]=['']+df1['Id of author of comment.'].apply(str).tolist()
        self.g1.vs["text"]=['']+df1['text'].tolist()
        self.g1.vs["likes"]=[0]+df1['likes'].tolist()
        self.g1.vs["date"]=[0]+df1['date'].tolist()
        for item in df1.iterrows():
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
                    pass
            else:
                #print(item[1])
                self.g1.add_edge('root',str(item[1]['Id of comment.']))

    def show(self):
        print(self.g1)
        layout = self.g1.layout("tree", root=[0])
        g.plot(self.g1, layout=layout)#, vertex_color = ["blue"]+["red"]*37)

gr=Intent_graph()
gr.parse('comm_politru_2_23812.csv')
gr.show()
