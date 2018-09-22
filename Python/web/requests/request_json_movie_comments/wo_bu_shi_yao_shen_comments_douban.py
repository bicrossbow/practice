import requests
import re #regular expression
import time
import random
import pandas as pd
from lxml import etree
from tqdm import tqdm

movie_name = ""
name_list, content_list, date_list, score_list, city_list = [], [], [], [], []

def get_city(url, i):
    time.sleep(round(random.uniform(2, 3), 2))
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    cookies = {'cookie':'bid=28NOW0qROeQ; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=DDC7944A482586D915A04C6958ABE488E|7aeae6cf8a5f1128707f0cb3e025cfc5; gr_user_id=d4dae539-4255-44b3-a8e6-591caeee4ac7; viewed="10564643_1052241"; ll="108258"; ps=y; ue="crossbow.zn@gmail.com"; __utma=30149280.1610953120.1531988116.1532577804.1532580962.5; __utmz=30149280.1532580962.5.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/bind_resetpassword; __utmt=1; _ga=GA1.2.1610953120.1531988116; _gid=GA1.2.1628709618.1532580966; _gat_UA-7019765-1=1; dbcl2="45871475:c5fQzRFB0Jc"; ck=9EAz; push_noty_num=0; push_doumail_num=0; __utmv=30149280.4587; __utmb=30149280.5.10.1532580962; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1532580988%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.204361065.1531988116.1532577804.1532580988.4; __utmb=223695111.0.10.1532580988; __utmz=223695111.1532580988.4.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=29e2cd51501420f5.1531988116.4.1532580992.1532578068.'}
    res = requests.get(url, cookies=cookies, headers=headers)
    if (res.status_code == 200):
        print("\n成功获取第{}个用户城市信息！".format(i))
    else:
        print("\n第{}个用户城市信息获取失败".format(i))
    pattern = re.compile('<div class="user-info">.*?<a href=".*?">(.*?)</a>', re.S)
    item = re.findall(pattern, res.text)  # list类型
    return (item[0])  # 只有一个元素，所以直接返回

def get_page_content(id_movie,idx_page):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    # cookies is needed, need to use use specific cookies
    # open chrome, click inspect, and reload the webpage
    # click the first item on the list, cookies will be listed on the right hand
    cookies = {'cookie':'bid=28NOW0qROeQ; __utmc=30149280; __utmc=223695111; _vwo_uuid_v2=DDC7944A482586D915A04C6958ABE488E|7aeae6cf8a5f1128707f0cb3e025cfc5; gr_user_id=d4dae539-4255-44b3-a8e6-591caeee4ac7; viewed="10564643_1052241"; ll="108258"; ps=y; ue="crossbow.zn@gmail.com"; __utma=30149280.1610953120.1531988116.1532577804.1532580962.5; __utmz=30149280.1532580962.5.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/bind_resetpassword; __utmt=1; _ga=GA1.2.1610953120.1531988116; _gid=GA1.2.1628709618.1532580966; _gat_UA-7019765-1=1; dbcl2="45871475:c5fQzRFB0Jc"; ck=9EAz; push_noty_num=0; push_doumail_num=0; __utmv=30149280.4587; __utmb=30149280.5.10.1532580962; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1532580988%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.204361065.1531988116.1532577804.1532580988.4; __utmb=223695111.0.10.1532580988; __utmz=223695111.1532580988.4.4.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=29e2cd51501420f5.1531988116.4.1532580992.1532578068.'}
    url = "https://movie.douban.com/subject/" + str(id_movie) + "/comments?start=" + str(idx_page * 10) + "&limit=20&sort=new_score&status=P"
    res = requests.get(url,headers = headers,cookies = cookies)
    
    res.encoding = "utf-8"
    if (res.status_code == 200):
        print("\n第{}页短评爬取成功！".format(idx_page + 1))
        print(url)
    else:
        print("\n第{}页爬取失败！".format(idx_page + 1))
        #TODO: raise error and return

    pattern = re.compile('<div id="wrapper">.*?<div id="content">.*?<h1>(.*?) 短评</h1>', re.S)
    global movie_name
    list_movie_name_found = re.findall(pattern, res.text)
    if(len(list_movie_name_found)>0):
        movie_name = list_movie_name_found[0]  # list type
    else:
        #TODO: need to raise an error
        pass
    
    with open('html.html','w',encoding = 'utf-8') as f:
        # write the page into local file to debug
        f.write(res.text)
        f.close  

    element_tree  = etree.HTML(res.text)
    for i in range(1,21):
        name = element_tree.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a/text()'.format(i))
        # 下面是个大bug，如果有的人没有评分，但是评论了，那么score解析出来是日期，而日期所在位置spen[3]为空
        score = element_tree.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[2]/@title'.format(i))
        date = element_tree.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/span[3]/@title'.format(i))
        m = '\d{4}-\d{2}-\d{2}'
        try:
            match = re.compile(m).match(score[0])
        except IndexError:
            break
        if match is not None:
            date = score
            score = ["null"]
        else:
            pass
        content = element_tree.xpath('//*[@id="comments"]/div[{}]/div[2]/p/span/text()'.format(i))
        id = element_tree.xpath('//*[@id="comments"]/div[{}]/div[2]/h3/span[2]/a/@href'.format(i))
        try:
            city = get_city(id[0], i)  # 调用评论用户的ID城市信息获取
        except IndexError:
            city = " "
        name_list.append(str(name[0]))
        score_list.append(str(score[0]).strip('[]\''))  # bug 有些人评论了文字，但是没有给出评分
        date_list.append(str(date[0]).strip('[\'').split(' ')[0])
        content_list.append(str(content[0]).strip())
        city_list.append(city)

def spider_douban_comments(id_movie,num_page_comments):
    global movie_name
    for i in tqdm(range(0, num_page_comments)):  # 豆瓣只开放500条评论
        get_page_content(id_movie, i)  # 第一个参数是豆瓣电影对应的id序号，第二个参数是想爬取的评论页数
        time.sleep(round(random.uniform(3, 5), 2))
    infos = {'name': name_list, 'city': city_list, 'content': content_list, 'score': score_list, 'date': date_list}
    data = pd.DataFrame(infos, columns=['name', 'city', 'content', 'score', 'date'])
    data.to_csv(movie_name + ".csv")  # 存储名为  电影名.csv

if __name__ == '__main__':
    id_movie = 26752088
    num_page_comments = 49
    #spider_douban_comments(id_movie,num_page_comments)
    spider_douban_comments(id_movie,num_page_comments)