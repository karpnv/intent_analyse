# -*- coding: utf-8 -*-
import vk_api
import pandas as pd

def session():
    """ Пример получения последнего сообщения со стены """

    login, password = '+79506072152', 'Sitn102O'
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    """ VkApi.method позволяет выполнять запросы к API. В этом примере
        используется метод wall.get (https://vk.com/dev/wall.get) с параметром
        count = 1, т.е. мы получаем один последний пост со стены текущего
        пользователя.
    """
    return vk


def request():
    response = vk.wall.getComments(owner_id=-25106701, post_id=441511, count=100, sort='asc')  # , offset=0
    if response['items']:
        com=pd.DataFrame(response['items'])
        print(com.head())

if __name__ == '__main__':
    vk = session()
    response = request()

