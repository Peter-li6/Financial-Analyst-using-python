# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 13:19:10 2022

@author: lipet
"""

import scrapy
import csv
 

class yahooSpider(scrapy.Spider):
    #name of our crawler will beyahoo
    name = "yahoo"
    
    #The urls to be scraped 
    start_urls = ["https://finance.yahoo.com/quote/MSFT/"]
    
    def parse(self,response):
        data = response.xpath('//div[@id="quote-summary"]/div/table/tbody/tr')
        
        if data:
            values = data.css('*::text').getall()
            
            filename = 'MSFTquote.csv'
            
            if len(values) != 0:
                with open(filename, 'a+', newline ='') as file:
                    f = csv.writer(file)
                    for i in range(0, len(values[:24]), 2):
                        f.writerow([values[i], values[i+1]])
                         
 
      