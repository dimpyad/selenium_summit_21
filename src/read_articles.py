import time

from selenium import webdriver
from configparser import ConfigParser

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = ConfigParser()
config.read('config.ini')

'''
This method will create a clean reading page from any article link
using http://outline.com
'''
def read_article():
    '''
    Opening chrome in headless mode
    '''
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    outline_url = config.get("links", "outline_url")
    article_url = config.get("links", "article_url")
    '''
    Creating an outline for a page using https://outline.com
    '''
    driver.get(outline_url)
    driver.find_element_by_id('source').send_keys(article_url)
    driver.find_element_by_class_name('clean').click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "copy-target"))
    )
    current_url = driver.current_url
    '''
    Opening chrome in normal mode
    '''
    driver = webdriver.Chrome('./chromedriver')
    driver.maximize_window()
    '''
    Opening the original url
    '''
    driver.get(article_url)
    time.sleep(5)
    '''
    Opening the clean URL after applying outline
    '''
    driver.get(current_url)
    time.sleep(5)
    driver.close()
    return current_url

if __name__ == '__main__':
    print(read_article())