import pandas as pd
import numpy as np
from datetime import datetime
min_d=datetime.strptime('01.01.2015 00:00:00', '%d.%m.%Y %H:%M:%S')
max_d=datetime.strptime('01.01.2016 00:00:00', '%d.%m.%Y %H:%M:%S')

def read_comm(name):
    df=pd.read_csv(name+'_comm.csv', sep=';', encoding='cp1251')
    df_post=pd.read_csv(name+'_posts.csv', sep=';', encoding='cp1251')

    post_set=set(df['Id of post'].values)
    num_2015=0
    num_new2015=0
    df_new = pd.DataFrame()
    df_post_new= pd.DataFrame()
    for ind in post_set:
        subdf=df[df['Id of post']==ind]#,['Id of author of comment.','date']
        #print('Индекс ',subdf.iloc[0,4])
        if type(subdf.iloc[0,4])==str:
            #print(type(subdf.iloc[0,4]))
            car_d=datetime.strptime(subdf.iloc[0,4], '%d.%m.%Y %H:%M:%S')
            if car_d>min_d and car_d<max_d and subdf.shape[0]<=30 and subdf.shape[0]>=20:
                num_2015+=1
                if True:#num_2015%3==0:

                    if df_new.shape[0]==0:
                        df_new=subdf.copy()
                        df_post_new=df_post[df_post['Id of post']==ind]
                    else:
                        df_new=pd.concat([df_new, subdf])
                        df_post_new=pd.concat([df_post_new,df_post[df_post['Id of post']==ind]])
                    num_new2015+=1
                #print(subdf.iloc[0,4], subdf.shape[0])
            else:
                pass


    print(num_2015, num_new2015)
    df_new.to_csv(name+'_comm_out_2.csv', encoding='cp1251', sep=';')
    df_post_new.to_csv(name+'_posts_out_2.csv', encoding='cp1251', sep=';')
    #df_new.to_excel(name+'_comm_out.xlsx',sheet_name='comm')
    #df_post_new.to_excel(name+'_posts_out.xlsx',sheet_name='posts')
    #print(df_new.shape)

def split_msg(name='inosmi2/-25106701'):
    df=pd.read_csv(name+'_comm_out_2.csv', sep=';', encoding='cp1251')
    df_post=pd.read_csv(name+'_posts_out_2.csv', sep=';', encoding='cp1251')
    post_set=set(df['Id of post'].values)
    new_com={}
    new_post={}
    for i,ind in enumerate(post_set):
        if True:#i >=75 and i<158:#158
            print(i)
            new_com[i]=df[df['Id of post']==ind]
            if 0 in new_post:
                new_post[0]=pd.concat([new_post[0],df_post[df_post['Id of post']==ind]])
            else:
                new_post[0]=df_post[df_post['Id of post']==ind]

            new_com[i].to_csv(name+'/comm_rosbalt_'+str(40+i)+'_'+str(ind)+'.csv', encoding='cp1251', sep=';')
            # if i%5 in new_com:
            #     new_com[i%5]=pd.concat([new_com[i%5],df[df['Id of post']==ind]])
            #     new_post[0]=pd.concat([new_post[0],df_post[df_post['Id of post']==ind]])
            # else:
            #     new_com[i%5]=df[df['Id of post']==ind]
            #     new_post[0]=df_post[df_post['Id of post']==ind]
        else:
            pass
    # print(new_com)
    # for i in new_com:
    #     new_com[i].to_csv(name+'/comm_25-75x5_'+str(i)+'.csv', encoding='cp1251', sep=';')

    new_post[0].to_csv(name+'/posts_rosbalt.csv', encoding='cp1251', sep=';')

#read_comm('inosmi2/-25106701')
#read_comm('politru/-21337773')
#split_msg('inosmi2/-25106701')
#read_comm('rosbalt/-32803139')
#split_msg('rosbalt/-32803139')
split_msg('politru/-21337773')