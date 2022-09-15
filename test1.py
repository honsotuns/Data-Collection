from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from ctypes import c_void_p
import os
import time
# from selenium.webdriver.support.ui import webDriverWait
# from selenium.webdriver.support import expected_condition as EC
from selenium.common.exceptions import TimeoutException
from uuid import uuid4
import json
import urllib
import pandas as pd 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC



class Scraper:

    def __init__(self, url):
        self.driver = webdriver
        self.url = url
        url = "https://www.lego.com/en-gb"
        

    def click_product(self):
        time.sleep(5)
        product_link = self.driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/header/div[2]/div[2]/div/div[3]/nav/div/div[1]/div/div[1]/ul/li[1]/a/span').get_attribute('href')
        print('link') 
        self.driver.get(product_link)
        
        
    
    def page_scroll(self):
        time.sleep(5)
        self.driver.execute_script("wondow.scrollTo(0, 10)")
        print("Page scrolled")


    def accept_cookies(self):
        time.sleep(2)
        try:
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/footer/div[3]/div/ul/li[2]/a/span') 
            accept_cookies_button.click()
            print('Cookies accepted')

        except AttributeError:
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="__next"]/footer/div[3]/div/ul/li[2]/a/span')
            accept_cookies_button.click()
            print('Attribute error')

    def extract_page_links(self):
        '''
        list_links = self.driver.find_elements(By.XPATH, 'common xpath')   #<ul> contains many <li> tags -> we want all the li tags because they have the href we need
        list_hrefs = []
        for link in list_links:       # go tot every elemnt in list_links and extract href 
            list_hrefs.append(link.get_attribute('href'))
       # return list_hrefs
        for href in list_hrefs:
            self.driver.get(href) 
        '''
        page_container = self.driver.find_elements(By.XPATH,'//*[@id="blt9495a15aac0c2092"]/section/div/div[2]/div/div/nav/a[2]/svg')
        page_link_list = []
        for item in page_container:
            link_to_page = item.get_attribute('href')
            print("link_to_page")
            page_link_list.append(link_to_page)

        print(page_link_list)
        print(len(page_link_list))
        return page_link_list

    def retrieve_info(self):
        for i in range (1,10):
            self.driver.get(f"https://www.lego.com/en-gb/categories/new-sets-and-products?page={i}")
              

    # def initialise(url):
    # initialise = Scraper(url)
    # click_product = initialise.click_product()
    # page_scroll = initialise.page_scroll()
    # accept_cookies = initialise.accept_cookies()


if __name__ == '__main__':
    lego_scrape = Scraper("https://www.lego.com/en-gb")
    # lego_scrape = Scraper("https://www.lego.com/en-gb/product/great-pyramid-of-giza-21058")
    lego_scrape.accept_cookies()
    lego_scrape.page_scroll()
    lego_scrape.click_product()
    lego_scrape.page_links()
    lego_scrape.retrieve_info()

    from timeit import timeit
    result = timeit(stmt='total=sum(range(100))',number=200)
    print(result/200)

    def count_ways(n:int)-> int:
        if (n==1 or n==0):
            return 1
        elif (n==2):
            return 2
        else:
            return count_ways(n-3) + count_ways(n-2) + count_ways(n-1)

    n=4
    print(count_ways(n))



    
        
        

        







    
