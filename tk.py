# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 19:48:11 2015
"""

from lxml.html.clean  import Cleaner
import lxml.html as html
import re 

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
        remove_print = r'Print options   Print:     Include Comments (.*)    Include images'
        article = re.sub(remove_print,"",article,count=1)
        remove_nextline = "\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\t\r"
        article = article.replace(remove_nextline,"",1)
        
        article = article.encode('utf8')
        self.article = article


        

if __name__ == "__main__":
    
    test = scraper("http://learningenglish.voanews.com/articleprintview/2717607.html")
    test.txtsave('tk.txt')


