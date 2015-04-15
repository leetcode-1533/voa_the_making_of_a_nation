# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:48:11 2015
"""

from lxml.html.clean  import Cleaner
import lxml.html as html
import re 
import os

import urllib2

class scraper:
    
    def __init__(self,link):
        self.link = link
        self.crawing()
        self.html2string()
            
    def crawing(self):
        response = urllib2.urlopen(self.link)
        self.plain_html = response.read()
#        wd = webdriver.Firefox()
#        wd.get(self.link)   
#        self.plain_html = wd.page_source
#        
#        wd.close()
    
    def txtsave(self,name_of_the_file):
        text_file = open(name_of_the_file,'w')
        text_file.write(self.article)
        text_file.close()
        
    def html2string(self):
        plain_html = html.document_fromstring(self.plain_html)
        Cleaner(kill_tags=['noscript'], style=True)(plain_html)
        
        article = plain_html.text_content()
#        self.test = plain_html.text_content()
        
        remove_print = r'Print options   Print:     Include Comments (.*)    Include images'
        article = re.sub(remove_print,"",article,count=1)
        # There is a large open space in the opening paragraph        
        remove_nextline = "(\r\n){10,}" 
        article = re.sub(remove_nextline,"",article,count=1)
        
        article = article.encode('utf8')
        self.article = article
        
    def mp3_download(self):
        test = 'file:///Users/y1275963/Downloads/8ff36304-8862-4091-84d9-be0b9bca5281_hq.mp3'
        mp3 = urllib2.urlopen(test)
        open('tk.mp3','wb').write(mp3.read())
        


        

if __name__ == "__main__":
    
    test = scraper("http://learningenglish.voanews.com/articleprintview/2711784.html")
    test.txtsave('tk.txt')


