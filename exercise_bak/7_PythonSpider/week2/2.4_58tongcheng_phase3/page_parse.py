from bs4 import BeautifulSoup
import requests
import time
from pymongo import MongoClient

host = 'localhost'
port = 27017

# 创建一个数据库client
client = MongoClient(host,port)
# 创建一个数据库,名为58tongcheng
db = client['bj_58tongcheng']
# 给数据库添加collection
sheet_url = db['urls']
sheet_item = db['items']

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
}

proxies = {'https':'https://166.78.3.170:9999'}

def get_item_urls(cate_url,page,who_sell=0,):
    url_list_view = '{}{}/pn{}'.format(cate_url,str(who_sell),str(page))
    print(url_list_view)
    wb_data = requests.get(url_list_view,headers=headers,proxies=proxies)
    soup = BeautifulSoup(wb_data.text,'lxml')
    time.sleep(1)

    # 去掉那些没有的页面,比如100页之后就是空的,所以不再爬取
    if soup.find_all('div',class_='noinfotishi'):
        pass
    else:
        links = soup.select('td.t > a.t')
        for link in links:
            # 判断是否为精准解析,通过对比分析发现,如果a的上上层父类,包含了zzjingzhun这个类的话,就是精准分析,我们过滤掉这部分的内容
            # 后来又发现还有一些分期付款的item,也将其过滤掉
            if len(link.find_parents("tr", class_="zzjingzhun")) or len(link.find_parents("tr", class_="fenqi_tr")) or len(link.find_parents("div", class_="zhiding")):
                pass;
            else:
                data = {
                    'title': link.get_text(),
                    'url': link.get('href'),
                }

                # url数据库断点设计
                if data['url'] in [item['url'] for item in sheet_url.find()]:
                    print('\n之前已经爬取了该url,跳过...\n')
                    pass
                else:
                    sheet_url.insert_one(data)
                    print(data)

'''
for page in range(1,2,1):
    get_item_urls('http://bj.58.com/shouji/',page)
'''
def get_item_details(url):
    wb_data = requests.get(url,headers=headers,proxies=proxies)
    soup = BeautifulSoup(wb_data.text,'lxml')
    time.sleep(1)

    no_longer_exist = '404' in soup.find_all('script',type="text/javascript")[-1].get('src').split('/')
    if no_longer_exist:
        pass
    else:
        title = soup.title.text
        price = soup.select('span.price_now > i')[0].get_text() if soup.find_all('span',class_='price_now') else None
        area = soup.select('div.palce_li > span > i')[0].get_text() if soup.find_all('div', 'palce_li') else None
        want_person = list(soup.select('span.want_person')[0].get_text())[0] if soup.find_all('span',class_='want_person') else None

        data = {
            'title':title,
            'price':price,
            'area':area,
            'want_person':want_person,
            'url':url
        }
        print(data)
        sheet_item.insert_one(data)

# for item in sheet_url.find().limit(2000):
#     get_item_details(item['url'])
