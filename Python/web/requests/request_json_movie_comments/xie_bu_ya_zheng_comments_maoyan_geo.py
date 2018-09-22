#coding=utf-8

from pyecharts import Style
from pyecharts import Geo

import os


def get_dic_city_name_count(list_city):
    dic_city_name_count = {}
    for city in set(list_city):
        dic_city_name_count[city] = list_city.count(city)
    return dic_city_name_count

if __name__ == '__main__':

    file_name_comments_org = 'xie_bu_ya_zheng_comments_remove_dup.txt'
    file_name_comments = 'xie_bu_ya_zheng_comments_remove_dup_backup.txt'
    os.system('cp {scr} {des}'.format(scr=file_name_comments_org,des=file_name_comments))
    
    # load city info
    city = []
    with open(file_name_comments,mode='r',encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            items_in_a_row = row.split(',')
            if len(items_in_a_row) == 5 and len(items_in_a_row[2])>=1:
                city.append(items_in_a_row[2].replace('\n',''))

    city_num_comment_pair = []

    style = Style(title_color = "#fff",title_pos = "center",width = 1200,height = 600,background_color = "#404a59")
    geo = Geo("《邪不压正》粉丝人群地理位置","数据来源：恋习Python",**style.init_style)

    dic_city_name_count = get_dic_city_name_count(city)
    for city_name in dic_city_name_count:
        coordinate=geo.get_coordinate(city_name)
        if coordinate is not None:
            city_num_comment_pair.append((city_name,dic_city_name_count[city_name]))
            #style = Style(title_color = "#fff",title_pos = "center",width = 1200,height = 600,background_color = "#404a59")
        else:
            print('{city} coordinate is not specified. Skip this city'.format(city=city_name))

    attr,value= geo.cast(city_num_comment_pair)
    # geo.add_coordinate("启东", 121.703, 31.87)
    # geo.add_coordinate("新昌", 120.9039, 29.4998)
    # geo.add_coordinate("璧山", 106.2273, 29.5920)
   
    geo.add("",attr,value,\
    visual_range=[0, 20], \
    maptype='china',\
    visual_text_color="#fff",\
    symbol_size=10,\
    is_visualmap=True,\
    is_piecewise=True,\
    visual_split_number=4)
    try:
        geo.render("邪不压正-评论分布.html")
    except ValueError as e:
        print(e)
   