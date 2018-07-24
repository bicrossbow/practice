"""
This is to study request and url to get data from online json 'database' and then use Geo to plot data visualization

https://www.jiqizhixin.com/articles/2018-07-22
"""


#coding=utf-8
import requests
import json
import time
import random

def get_one_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    print(type(response))
    print(response)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    content = json.loads(html)
    data = content['cmts']
    for item in data:
        yield{
            'comment':item['content'],
            'date':item['time'].split(' ')[0],
            'rate':item['score'],
            'city':item['cityName'],
            'nickname':item['nickName']
        }

def save_to_text(file_name):
    page_start = 479
    page_end = 1001
    for i in range(479,page_end):
        url = 'http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset=' + str(i)
        html = get_one_page(url)
        print('Saving page{}'.format(i))
        for item in parse_one_page(html):
            with open(file_name,'a',encoding='utf-8') as f:
                f.write('{date},{nickname},{city},{rate},{comment}\n'.format(date=item['date'],nickname=item['nickname'],city=item['city'],rate=item['rate'],comment=item['comment'].replace('\n',' ')))
                #f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' +str(item['rate'])+','+item['comment']+'\n')
        time.sleep(5 + float(random.randint(1, 100)) / 20)

def remove_dupline(infile,outfile):
    infopen = open(infile,'r',encoding='utf-8')
    outopen = open(outfile,'w',encoding='utf-8')
    lines = infopen.readlines()
    list_line = []

    for line in lines:
        if line not in list_line:
            list_line.append(line)
            outopen.write(line)
    infopen.close()
    outopen.close()

if __name__ == '__main__':
    file_name = 'xie_bu_ya_zheng_comments.txt'
    file_name_no_dup = 'xie_bu_ya_zheng_comments_remove_dup.txt'
    save_to_text(file_name)
    remove_dupline(file_name,outffile_name_no_dupile)
    