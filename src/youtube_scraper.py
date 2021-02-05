import  time
from selenium import webdriver
from configparser import ConfigParser

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = ConfigParser()
config.read('config.ini')

'''
This method will return the list of top videos from any youtube channel 
and will play the last uploaded video
'''
def open_video_from_youtube():
	url = config.get("links","youtube_url") + config.get("links","youtube_channel")
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./chromedriver', options=chrome_options)
	driver.maximize_window()
	driver.get(url)
	height = driver.execute_script("return document.documentElement.scrollHeight")
	lastheight = 0

	while True:
		if lastheight == height:
			break
		lastheight = height
		driver.execute_script("window.scrollTo(0, " + str(height) + ");")
		time.sleep(2)
		height = driver.execute_script("return document.documentElement.scrollHeight")

	user_data = driver.find_elements_by_xpath('//*[@id="video-title"]')

	count = 0
	link_to_play = None
	for i in user_data:
		print(i.get_attribute('href'))
		link = (i.get_attribute('href'))
		if count == 0:
			link_to_play = link
		count += 1
	driver = webdriver.Chrome('./chromedriver')
	driver.maximize_window()
	print (link_to_play)
	driver.get(link_to_play)
	WebDriverWait(driver, 15).until(EC.element_to_be_clickable(
		(By.XPATH, "//button[@aria-label='Play']"))).click()
	time.sleep(5)
	driver.close()

if __name__ == '__main__':
	open_video_from_youtube()
