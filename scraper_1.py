from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine
from urllib.parse import urlparse, parse_qs, urlencode
import os
import json
import urllib.request
import time
import uuid
import boto3
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as bs
import requests


class GMS:
    '''
    This class is used to represent the Gorilla Mind website to be scraped.
    Attributes:
    url (str): The url link to the website to be scraped.
    '''
    
    def __init__(self, url):
        '''
        Constructs the necessary attributes for the scraper object and sets the webdriver to Selenium.
        
        Parameters:
        url (str): The url link to the website to be scraped.
        '''
        self.url = url
        options = Options()
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.s3_client = boto3.client('s3')

    def open_page(self):
        '''
         This function is used to open the webpage given.
        '''
        self.driver.get("url")
    

    def access_shop_all(self, driver):
        '''
        This function is used to click on a products.
        '''
        driver.get("https://gorillamind.com/collections/all-products") 
        wait = WebDriverWait(driver,30)
        options = driver.find_element("//ul[@class='product-list-tiles row list-unstyled']/li")
        print(len(options))
        count = 0
        try:
            while True:
                if count > 5: 
                    break
                moreoption = wait.until(EC.element_to_be_clickable((By.XPATH,"///html/body/div[3]/header/nav/div/div/div/div[2]/nav/a[1]']")))
                driver.execute_script("arguments[0].scrollIntoView(true);",moreoption)
                driver.execute_script("window.scrollBy(0,-300);")
                time.sleep(2)
                moreoption.click()
                count += 1
                time.sleep(2)
                options = driver.find_elements_by_xpath("//ul[@class='product-list-tiles row list-unstyled']/li")
                print(len(options))
        except:
            pass 

    def scroll_to_next_page_button(self, driver):
        '''
        This function is used to scroll down to the next page button.
        '''
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.scroll_to_next_page_button(driver)

    
    def get_product_data(self, link):
        '''
        This function is used to create a dictionary containing all product data.
        Parameters:
        link (str): The link to the product page.
        Returns:
            dict: The dictionary containing all product data.
        '''
        product_dict = {'Name': '', 'ID': '', 'UUID': '', 'Price': 0, 'Description': '', 'Number of Flavours': [], 'Rating': 0, 'Image Link': ''}
        self.driver.get(link)
        product_dict['ID'] = self.product_id(link)
        UUID = str(uuid.uuid4())
        UUID_1 = UUID.strip("UUID('")
        UUID_2 = UUID_1.strip(")'")
        product_dict['UUID'] = UUID_2
        product_dict['Image Link'] = self.extract_image_link(link)
        try:
            product_dict['Name'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/h1').text
        except:
            print('Name not found.')
        
        try:
            product_dict['Price'] = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[1]/section/div/div/div[2]/div[1]/p/span[2]/span/span').text
        except:
            print('Price not found.')

        try:
            descrip_txt = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-product__supplements"]/section[2]/div/div/div[1]/div/div[1]/div[1]/span[1]').text
            description = descrip_txt.replace('\n', " ")
            product_dict['Description'] = description
        except:
            print('Description not found.')

        try:
            flavours = self.driver.find_element(by=By.XPATH, value='//*[@id="product_form_4891279261741"]/div[2]/div[1]').text
            flavour_list = flavours.splitlines()
            flavour_list.remove('Flavor')
            product_dict['Number of Flavours'] = len(flavour_list)
        except:
            print('Flavours not found.')
        
        try:
            rating = self.driver.find_element(by=By.XPATH, value='//*[@id="shopify-section-68eb7e26-87f6-4711-8408-2327df293f70"]/section/div/div/div/div/span/div[1]/div/div[1]/span').text
            rating = float(rating)
            product_dict['Rating'] = rating
        except:
            print('Rating not found.')
        
        return product_dict

    
    def product_id(self, link):
        '''
        This function is used to generate a product ID from its web address.
        
        Parameters:
            link(str): The link to the product page.
            '''
        
        id = link.replace('https://gorillamind.com/collections/all/products/', '')
        if id[0:5] == 'https':
            id = link.replace('https://gorillamind.com/products/', '')    
        return id

    def make_directory(self, path):
        '''
        This function is used to create a local folder for a given product in a specificed location.
        
        Parameters:
            path(str): The path to the local folder.
        '''
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)

    def get_path_to_data(self, link):
        '''
        This function is used to create the path to the local folder for a given product from its product page link.
        
        Parameters:
            link(str): The link to the product page.
        '''
        id = self.product_id(link)
        cwd = os.getcwd()
        path = f'{cwd}/raw_data/{id}' 
        return path

    def download_image(self, link, path):
        '''
        This function is used to save a product image in a specified directory.
        
        This function retrives a product's image through the link in its dictionary and saves
        the image within the specified directory.
        '''
        image_link = self.extract_image_link(link)
        id = self.product_id(link)
        os.chdir(path)
        urllib.request.urlretrieve(image_link, f"{id}.jpeg")

    

    def save_data(self, data, directory):
        '''
        This function is used to save the data of a product in a specified directory.
        '''
        os.chdir(directory)
        with open('data.json'.format(name = data["ID"]), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    
    def close_page(self):
        '''
        This function is used to quit the browser.
        '''
        self.driver.quit()
       
    
        
if __name__ == '__main__':
    scraper = GMS('https://gorillamind.com')
    data = scraper.get_product_data('https://gorillamind.com')
    path = scraper.get_path_to_data('https://gorillamind.com/collections/all-products')
    directory = scraper.make_directory(path)
    scraper.save_data(data, path)
    scraper.download_image('https://gorillamind.com/products/gorilla-mode-nitric', path)
    df = pd.DataFrame(data, index=[0])
    print(df)
    scraper.close_page()
        