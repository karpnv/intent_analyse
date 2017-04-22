# coding=utf-8

import igraph as g
import pandas as pd
import os
import logging
import re
import numpy

class Intent_graph():
    def __init__(self, dir='with_tags'):
        logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO)
        self.dir=dir#'politru/-21337773_1/'
        self.pattern=re.compile('\W')
    def sub(self, str1):
        try:
            return self.pattern.sub('', str(str1))
        except:
            return ''
    def parse(self, f_name='comm_politru_2_23812.csv'):
        g1 = g.Graph(directed=True)
        g1.add_vertices(1)
        df0=pd.read_csv(f_name, encoding='cp1251', sep=';', header=0)#cp1251#UTF-8
        k=df0.shape[0]
        df0['target']=['']*k
        df0['id']=df0['Id of comment.']
        df1=df0.copy()

        for j,item in enumerate(df0.ix[:,-4].fillna('')):
            #print('i',item)
            il=item.split(',')
            if len(il)>1:
                flag=True
                for ii,it in enumerate(il):
                    s=self.pattern.sub('', it).lower()
                    if len(s)>1:
                        if flag:
                            df1.iloc[j,-4]=s[0]
                            df1.target[j]=s[1]
                            flag=False
                        else:
                            df3=df0.iloc[j,:].copy()
                            df3.iloc[-4]=s[0]
                            df3.target=s[1]
                            df3.name=k
                            df3.id=df3.id*1000+ii
                            df1=df1.append(df3)
                            k+=1
            elif len==0:
                df1.iloc[j,-4]=''
            else:
                s=self.pattern.sub('', item).lower()
                if len(s)>1:
                    df1.iloc[j,-4]=s[0]
                    df1.target[j]=s[1]
        #print(df1)

        root=df1.loc[0,'Id of post']
        g1.add_vertices(df1.shape[0])
        g1.vs['id']=[root]+df1['id'].tolist()
        g1.vs["name"]=[str(root)]+df1['id'].fillna('').apply(str).tolist()
        g1.vs["Label"]=[str(root)]+df1['Id of comment.'].fillna('').apply(str).tolist()
        g1.vs["author"]=['']+df1['Id of author of comment.'].fillna('').apply(str).tolist()
        g1.vs["text"]=['']+df1['text'].fillna('').tolist()
        g1.vs["likes"]=[0]+df1['likes'].tolist()
        g1.vs["date"]=['']+df1['date'].fillna('').tolist()
        g1.vs["intent"]=['0']+df1.ix[:,-4].fillna('').tolist()
        g1.vs["target"]=['0']+df1['target'].fillna('').tolist()
        g1.vs["content"]=['']+df1.ix[:,-3].fillna('').apply(self.sub).tolist()#

        #print(g1.vs["date"])
        for item in df1.iterrows():
            try:
                start,stop=item[1]['text'].find('[id'),item[1]['text'].find('|')
                if start>=0 and stop>=0:
                    #print(item[1]['text'][start+3:stop])
                    authors_messages=df1[
                        df1['Id of author of comment.']==int(item[1]['text'][start+3:stop])][
                        df1['Id of comment.']<item[1]['Id of comment.']][
                        ['Id of comment.','id']]
                    if authors_messages.shape[0]>0:
                        id_list=authors_messages[authors_messages['Id of comment.']==
                                  authors_messages['Id of comment.'].values[-1]]['id'].values
                        #last_authors_message=authors_messages['id'].values[-1]
                        for last_authors_message in id_list:
                            g1.add_edge(str(last_authors_message),str(item[1]['id']))
                    else:
                        #создать вершину которая отсутствует и добавить ребро от нее
                        pass
                else:
                    g1.add_edge(str(root),str(item[1]['id']))
            except AttributeError:
                #logging.info('Empty message in line \n %s', item[1])
                pass


        return g1

    def print_pdf(self, g1, fname):
        #print(fname, g1)
        layout = g1.layout("tree", root=[0])
        visual_style={}
        visual_style["layout"] = layout
        #visual_style["vertex_label"] = g1.vs["name"]
        #visual_style["vertex_label_dist"] = -4
        #visual_style["bbox"] = (300, 300)

        g.plot(g1, fname+'.pdf', **visual_style)

        #g.plot(self.g1, layout=layout)#, vertex_color = ["blue"]+["red"]*37)


    def iter_dir(self, func, ext_name='.csv', group_id=0):
        graph_dict={}
        i=0
        for name in sorted(os.listdir(self.dir)):
            path = os.path.join(self.dir, name)
            if os.path.isdir(path):
                for fname in sorted(os.listdir(path)):
                    if group_id==0:
                        if fname[-4:]==ext_name:
                            fpath = os.path.join(path, fname)
                            logging.info('fpath %s', fpath)
                            g1=func(fpath)
                            graph_dict[i]=g1#fname[:-4]
                            i+=1
                    else:
                        if fname[-4:]==ext_name and fname[0]==str(group_id):
                            fpath = os.path.join(path, fname)
                            logging.info('fpath %s', fpath)
                            g1=func(fpath)
                            graph_dict[i]=g1#fname[:-4]
                            i+=1
        logging.info('i= %s', i)
        return graph_dict

    def write_gml(self, fpath):
        g1 = self.parse(fpath)
        g1.write_gml(fpath[:-4] + '.gml')
        self.print_pdf(g1,fpath[:-4])
        return g1

    def conv_xlsx(self, fpath):
        logging.info('fpath %s', fpath)
        df1=pd.read_excel(fpath)
        #print(df1)
        df1.to_csv(fpath[:-4]+'.csv', sep=';',index=True,header=True, encoding='cp1251')

    def read_gml(self, fpath):
        return g.Graph().Read_GML(fpath)

    def take_path(self, graph):
        print(graph)

    def generalise_letters(self, igraphs):
        generalization_rule = {"I": ["а", "б", "в", "г", "д"],  # Информативно-воспроизводящий
                               "E": ["е", "ж", "з", "и", "к"],  # Эмотивно-консолидирующий
                               "M": ["л", "м", "н", "о", "п"],  # Манипулятивный тип, доминирование
                               "D": ["р", "с", "т", "у", "ф"],  # Волюнтивно-директивный
                               "R": ["х", "ц", "ч", "ш", "щ"]}  # Контрольно-реактивный
        new_letter = {}
        new_letter['0']='0'
        new_letter[''] = ''
        for key in generalization_rule:
            for old_letter in generalization_rule[key]:
                new_letter[old_letter] = key
        for key in igraphs:
            l=[]
            for letter in igraphs[key].vs["intent"]:
                try:
                    l.append(new_letter[letter])
                except KeyError:
                    l.append('')
            if len(igraphs[key].vs["intent"])==len(l):
                igraphs[key].vs["g_intent"]=l
            else:
                logging.warning('Warning!, len(vs["intent"])!=len(l), key=%s',key)
        return igraphs

if __name__ == '__main__':
    gr=Intent_graph('with_tags')
    graph_dict=gr.iter_dir(gr.write_gml, '.csv')
    # graph_dict=gr.iter_dir(gr.read_gml, '.gml')
    print(len(graph_dict))
    # for key in graph_dict:
    #     print(key, graph_dict[key])
        #gr.take_path(graph_dict[key])

    #9-Шарова-comm_inosmi_25_197198 ???????