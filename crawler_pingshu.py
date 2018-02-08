import requests
from bs4 import BeautifulSoup
import lxml
from urllib import parse
from selenium import webdriver

def get_all_peoples():
    url = 'http://www.pingshu8.com/Music/bzmtv_1.Htm'
    people_list = []
    r = requests.get(url,timeout = 30)
    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text,'lxml')

    div_list = soup.find_all('div',class_='t2')[0]
    #div_list = soup.find_all('a')
    people_div_list = div_list.find_all('a')
    #city_link_list = city_div.find_all('a')
    for i in range(0,people_div_list.__len__()):
        people_name = people_div_list[i].text
        people_href = people_div_list[i]['href']
        people_list.append((people_name,people_href))
    return people_list

def get_pingshu_list(url):
    pingshu_list = []
    url ='http://www.pingshu8.com'+url
#    /Special/Msp_21.Htm'
    r = requests.get(url,timeout = 30)

    r.encoding = 'gb2312'
    soup = BeautifulSoup(r.text,'lxml')
    pingshu_div_list = soup.find_all('div',class_='tab33')

    for i in range(0,pingshu_div_list.__len__()-1):
        pingshu_name = pingshu_div_list[i].find('a').text
        pingshu_href = pingshu_div_list[i].find('a')['href']
        pingshu_list.append((pingshu_name,pingshu_href))
    return pingshu_list

def get_pingshu_downloadurl(url):
    # chromedriver = '/usr/lib/chromium-browser/chromedriver'
    phantomPath = '/home/eric/anaconda3/bin/phantomjs'
    browser = webdriver.PhantomJS(phantomPath)
    # Chrome(chromedriver)
    browser.get(url)
    elem = browser.find_elements_by_class_name('a1')
    downhref = browser.find_elements_by_class_name('a2')
    print(elem.__len__())
    for i in range(0,elem.__len__()):
        # range范围不包括最后一个数，不用减一
        print(i)
        print(downhref[i].find_element_by_tag_name('a').get_attribute('href'))
        print(elem[i].find_element_by_tag_name('a').get_attribute('innerHTML'))

    browser.close()
    # r = requests.get(url,timeout =30)
    # r.encoding = 'gb2312'
    # bs = BeautifulSoup(r.text,'lxml')
    # print(bs.text)
    # pingshu_download_list =[]
    # # dict/list 之间的区别
    # # pingshu_form = bs.find_all('form',name='form')[1]
    # pingshu_li = bs.find_all('li',class_='a1')
    # print(pingshu_li.__len__())
    # for i in range(0,pingshu_li.__len__()-1):
    #    # pingshu_download_list.append((pingshu_download_bs[i],text,pingshu_download_bs[i]['href']))
    #    # repeat this mistake so many times, need to find <a> further more
    #    name = pingshu_li[i].find('a').text,i
    #    href = pingshu_li[i].find('a')['href'],i
    #    pingshu_download_list.append((name,href))
    #    print(name,href)
    # return pingshu_download_list


def get_url(url):
    # jsString = 'pingshu://cc%252Fbzmtv%255FInc%252Fdownload%252Easp%253Ffid%253D102539akb%253D%253D'
    url = parse.unquote(parse.unquote(url[10:]))
    # print(jsString[2:-5])
    url = 'http://www.pingshu8.com' + url[2:-5]
    r = requests.get(url, timeout=30)
    print(url + '\n' + r.text + '*************')
"""
    var downurl ="pingshu://cc%252Fbzmtv%255FInc%252Fdownload%252Easp%253Ffid%253D102539akb%253D%253D"
    downurl=decodeURIComponent(decodeURIComponent(downurl.substr(10,downurl.length-1)))
    downurl=downurl.substr(2,downurl.length-7)
*********************************************************
    functions upon the line is the pingshu8.com's javascript function in web
"""

def main():

 city_list = get_all_peoples()
 i = 1
 all_actors = {}
 for city in city_list:
    city_name = city[0]
    city_pinyin = city[1]
    print(city_name,city_pinyin,i)
    psfile = open('pingshu.txt','a')
    psfile.write('({2})演员:{0},主页:{1}\n'.format(city_name,city_pinyin,i))
    pinglist = get_pingshu_list(city_pinyin)
    psfile.write('共{}部作品收录\n'.format(pinglist.__len__()))
    for name in pinglist:
        pingshu_href = name[1]
        pingshu_name = name[0]
        print(pingshu_name,pingshu_href)
        psfile.write('《{}》，链接：{}\n'.format(pingshu_name,pingshu_href))
        pingshu_download_list = get_pingshu_downloadurl(pingshu_href)
        for story in pingshu_download_list:
            psfile.write('{}，链接:{}\n'.format(story[0],story[1]))
    i+=1
    all_actors[city_name] = pinglist.__len__()
    psfile.write('*********************************************\n')
    psfile.close()

 for key in all_actors.keys():
     print(key,all_actors[key])

 # print(sorted(dict,key=lambda x:dict[x])[-1])

if __name__=='__main__':
    # main()
    # get_url('pingshu://cc%252Fbzmtv%255FInc%252Fdownload%252Easp%253Ffid%253D102539akb%253D%253D')
    pingshu_download_list = get_pingshu_downloadurl('http://www.pingshu8.com/MusicList/mmc_235_6576_1.Htm')
    # print(pingshu_download_list.__len__())
    # for story in pingshu_download_list:
    #     print('{}，链接:{}\n'.format(story[0], story[1]))
    #     #print(pingshu_download_list.__len__())