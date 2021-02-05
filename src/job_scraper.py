from bs4 import BeautifulSoup
import time
import random
from configparser import ConfigParser

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

config = ConfigParser()
config.read('config.ini')



def create_job_list_from_naukri():
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome('./chromedriver', options=chrome_options)
	url = config.get("links", "job_url")
	pages = int(config.get("links", "no_of_job_pages"))
	driver.maximize_window()
	#driver.get(url)

	Link = []
	for page in range(1, pages):
		driver.get(url + str(page))
		timeDelay = random.randrange(0, 5)
		time.sleep(timeDelay)
		soup = BeautifulSoup(driver.page_source, 'lxml')  # returns html of the page
		for i in soup.findAll(attrs={'class': "jobTuple bgWhite br4 mb-8"}):
			for j in i.findAll(attrs={'class': "title fw500 ellipsis"}):
				Link.append(j.get('href'))  # stores all the link of the job postings

	salary = []
	experience = []
	Location = []
	description = []
	role = []
	industry_type = []
	qualification = []
	Functional_area = []
	Employment_type = []
	Role_category = []
	company = []
	skills = []

	for lin in range(len(Link)):
		driver.get(Link[lin])
		# time.sleep(1)
		soup = BeautifulSoup(driver.page_source, 'lxml')
		if soup.find(attrs={'class': "salary"}) == None:  # to skip the error
			continue
		else:

			experience.append(soup.find(attrs={'class': "exp"}).text)
			salary.append(soup.find(attrs={'class': "salary"}).text)
			Location.append(soup.find(attrs={'class': 'loc'}).find('a').text)

			description.append(soup.find(attrs={'class': "job-desc"}).text)

			details = []

			for i in soup.find(attrs={'class': "other-details"}).findAll(attrs={'class': "details"}):
				details.append(i.text)

			role.append(details[0])
			industry_type.append(details[1])

			Functional_area.append(details[2])
			Employment_type.append(details[3])
			Role_category.append(details[4])

			qual = []
			for i in soup.find(attrs={'class': "education"}).findAll(attrs={'class': 'details'}):
				qual.append(i.text)
			qualification.append(qual)
			sk = []
			for i in soup.find(attrs={'class': "key-skill"}).findAll('a'):
				sk.append(i.text)
			skills.append(sk)

			company.append(
				soup.find(attrs={'class': "about-company"}).find(attrs={'class': "detail dang-inner-html"}).text)
	driver.close()

	df = pd.DataFrame()
	df['company'] = company
	df['role'] = role
	df['salary'] = salary
	df['experience'] = experience
	df['Location'] = Location
	df['description'] = description
	df['skills'] = skills
	df['qualification'] = qualification
	df['industry_type'] = industry_type

	df['Functional_area'] = Functional_area
	df['Employment_type'] = Employment_type
	df['Role_category'] = Role_category

	df.to_csv('naukri.csv', index=False)

if __name__ == '__main__':
    create_job_list_from_naukri()