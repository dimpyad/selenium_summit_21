from selenium import webdriver
import time
from configparser import ConfigParser

from selenium.webdriver.chrome.options import Options

config = ConfigParser()
config.read('config.ini')


def read_news():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    url = config.get("links", "news_url")
    driver.maximize_window()
    driver.get(url)
    time.sleep(3)
    news = driver.find_elements_by_class_name('hdg3')
    list = []
    count = 0
    for item in news:
        if count < 5 :
            list.append(item.text)
            count +=1
        else:
            break;

    driver.close()
    return list

if __name__ == '__main__':
    print(read_news())