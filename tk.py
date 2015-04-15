# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:48:11 2015
"""

from lxml.html.clean  import Cleaner
import lxml.html as html
import re 
import os
import datetime

import requests

from bs4 import BeautifulSoup
import urllib2

class scraper:
    
    def __init__(self,link):
        destionation = '/tmp'

        self.ori_link = link
        self.analyzer()
        
        #define the download path:
        self.loc = os.path.join(destionation,self.date)
        if not os.path.exists(self.loc):
            os.mkdir(self.loc)
        
        
        self.crawing()
        self.txtsave()
        self.mp3_download()
        
    def analyzer(self):
        
        # get print url:
        print_code = re.findall(r'\d+.html',self.ori_link)[0]
        print_patter = 'http://learningenglish.voanews.com/articleprintview/'  
        self.print_link = print_patter + print_code
        
        
        # get mp3 url:        
        response = requests.get(self.ori_link)
        
        if response.status_code != 200:
            print "Printing: Not 200"
        html = response.content                  
        soup = BeautifulSoup(html)      
        
        mp3list = soup.find('li',{'class':'downloadlink'})
        mp3list = mp3list.findAll('a',)
      
        # mp3list:
        # 0: MP3 - 128.0kb/s ~8.3MB
        # 1: wav - 1.4Mb/s ~ 91.3MB
        # 2: MP3 - 64.0kb/s ~4.1MB
        
        mp3_link = mp3list[0]
        self.mp3_link = mp3_link['href']
        
        # We can continue to use the soup:     
        # get the title:        
        self.title = soup.title.contents[0].strip().encode('utf8')
        
        # get the date:
        date_temp = soup.find('p',{'class':'article_date'})
        date = date_temp.contents[0].strip()
        ##change the format:
        self.date = datetime.datetime.strptime(date,'%m/%d/%Y').strftime('%y-%m-%d')
        
                  
    def txtsave(self):
        text_file = open(os.path.join(self.loc,self.title)+'.txt','w')
        text_file.write(self.article)
        text_file.close()
        
    def crawing(self):
        # This is to get the content of the audio
    
        response = requests.get(self.print_link)
        if response.status_code != 200:
            print "Printing: Not 200"
            
        plain_html = html.document_fromstring(response.content)
        
        Cleaner(kill_tags=['noscript'], style=True)(plain_html)
        
        article = plain_html.text_content()
        
        remove_print = r'Print options   Print:     Include Comments (.*)    Include images'
        article = re.sub(remove_print,"",article,count=1)
        # There is a large open space in the opening paragraph        
        remove_nextline = "(\r\n){10,}" 
        article = re.sub(remove_nextline,"",article,count=1)
        
        article = article.encode('utf8')
        self.article = article
        
    def mp3_download(self):
        mp3 = urllib2.urlopen(self.mp3_link)
        open(os.path.join(self.loc,self.title)+'.mp3','wb').write(mp3.read())
        


        

if __name__ == "__main__":
    
    ori_url = "http://learningenglish.voanews.com/content/americans-remember-lincoln-assassination-150-years/2717607.html"
    test = scraper(ori_url)


