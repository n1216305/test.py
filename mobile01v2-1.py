
# coding: utf-8

# In[2]:

import re
import codecs
import sys
import time
import datetime
import os
import requests
from lxml import html
import MySQLdb

connect=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="",db="mobile01",charset='utf8', use_unicode=False)

#寫入DB
def process_item(mobile01_url,Article_Name,_Article_Content):
    cursors=connect.cursor()
    #try:
    check = "SELECT url FROM news where url=%s"
    cursors.execute(check,[mobile01_url])
    if cursors.rowcount == 0 :
        sql="INSERT INTO news (url, title, content) VALUES (%s,%s,%s)"
        # (str(item['content']).encode("utf8"))
        cursors.execute(sql,(mobile01_url,Article_Name,_Article_Content))
        connect.commit()
    #except MySQLdb.Error,e:
    #    print "Error %d: %s" % (e.args[0], e.args[1])
    cursors.close()

def Article(Article_Url):
    content = requests.get(Article_Url).content
    tree = html.fromstring(content)
    
    _Article_Name = tree.xpath('//div[@class="forum-content"]/main/h1/text()')
    Article_Name = ''.join(_Article_Name).replace(" ","")
    print (Article_Name)
    
    #_Article_Date = tree.xpath('//div[@class="date"]/text()')
    #Article_Date = ''.join(_Article_Date).replace(" ","")
    #print (Article_Date)

    _Article_Content = tree.xpath('//div[@class="single-post-content"]/div/text()')
    #print (_Article_Content)

    Article_Content = ' '.join(_Article_Content).replace(" ","")
    print (Article_Content + '\n')
    print("---------------下一篇-----------------")#下一篇

    process_item(Article_Url,Article_Name,Article_Content)
    time.sleep(1)

def run_url():

    Today = time.strftime("%Y/%m/%d")
    Status = True
    Page = 1
    while Status:
        print ("第: " + str(Page) + "頁")
        _url = "http://www.mobile01.com/topiclist.php?f=291&p=" + str(Page)
        content = requests.get(_url).content
        tree = html.fromstring(content)

        All_Url = tree.xpath('//div[@class="tablelist forumlist"]//span[@class="subject-text"]/a/@href')
        
        #_Today_NEWS = tree.xpath('//div[@class="tablelist forumlist"]//span[@class="subject-text"]/a/text()')
        #Today_NEWS = ''.join(_Today_NEWS).replace(" ","")
        
        #print ("Apple_NEWS:" + Today_NEWS)
        #_classify = tree.xpath('//div[@class="abdominis rlby clearmen"]/ul/li/a/h2/text()')
        #classify = ' '.join(_classify).replace(" ","")
        #print (classify)

        #if (Today != Today_NEWS):
            #Status = False
            #print ("已經沒有了哦~~~看到表示為今日以前") #檢查是否為今天
        #elif (Page ==3):
            #print ("測試用指印到這") #測試印2頁
            #break
        #else:
        Page += 1
        for _u in All_Url:
            mobile01_url = "http://www.mobile01.com/" + _u + '\n'
            #print(Today_NEWS)
            print(mobile01_url)#網頁的網址
            Article(mobile01_url)
        print("---------------換頁-----------------")#換頁
        
        time.sleep(10)
        



if __name__ == "__main__":
    run_url()
connect.close()


# In[ ]:




# In[ ]:



