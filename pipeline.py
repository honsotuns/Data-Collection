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


# https://www.ocado.com/browse/m-s-at-ocado-294578?filters=organic-19997

class Scraper:

    def __init__(self, url):
        self.driver = webdriver.chrome()
        self.url = url
        url = "https://www.lego.com/en-gb/product/great-pyramid-of-giza-21058"
        # self.driver.get(URL) # error message
        pass

    def click_product(self):
        time.sleep(5)
        product_click = self.driver.find_element(By.XPATH,'//*[@id="main-content"]/div/div[1]/div/div[2]/div[2]/h1/span')
        link = product_click.get_attribute('href')
        print(link)
        self.driver.get(link)


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

        except:
            pass

    def page_links(self):
        page_link_list = []
        page_container = self.driver.find_elements(By.XPATH,)# Insert page link path

        for item in page_container:
            link_to_page = item.get_attribute('href')
            print("link_to_page")
            page_link_list.append(link_to_page)

        print(page_link_list)
        print(len(page_link_list))
        return page_link_list

def initialise(url):
    initialise = Scraper(url)
    click_product = initialise.click_product()
    page_scroll = initialise.page_scroll()
    accept_cookies = initialise.accept_cookies()




if __name__ == '__main__':
    initialise() # What should I call ?
    # lego_scrape = Scraper() # "https://www.lego.com/en-gb/product/great-pyramid-of-giza-21058")
    # lego_scrape.accept_cookies()
    # lego_scrape.page_scroll()
    # ego_scrape.click_product()
    # lego_scrape.page_links()





    
        
        

        







    
