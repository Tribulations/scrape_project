# -*- coding: utf-8 -*-
#import chromedriver_install as cdi
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
from createUniqueFile import createUniqueFile
import logging

# logging
logger = logging.getLogger('dynamicScrape')
logger.setLevel(logging.INFO) # you can set this to DEBUG, INFO, ERROR
# assign a file handlerto that instance
fh = logging.FileHandler("errorLog.txt")
fh.setLevel(logging.INFO)# again you can st his differently
# Format your logs (optional)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)# This will set the format to the FileHandler
# Add the handler to your loigging instance
logger.addHandler(fh)

try:
	file = open("/home/jocke/scrapeProject/log.txt", 'a')

	url = "http://www.nasdaqomxnordic.com/shares"
	driver = webdriver.Chrome("/usr/bin/chromedriver") # loads the driver? Maybe the path isn't needed?
	driver2 = webdriver.Chrome()

	driver.get(url) # retrieves the webpage?

	xpathSTO = "//*[@id=\"marketCheckboxes\"]/li[3]/label" # the path to the clickbox
	STOClickBox = driver.find_element_by_xpath(xpathSTO) # saves the element i var.
	STOClickBox.click() # clicks the element
	#xpathHEL = "//*[@id=\"marketCheckboxes\"]/li[4]/label"
	#xpathSmallCap = "//*[@id=\"nordicSegment\"]/ul/li[3]/label"
	#xpathMidCap = "//*[@id=\"nordicSegment\"]/ul/li[2]/label"
	#MidCapClickBox = driver.find_element_by_xpath(xpathMidCap)
	#HELClickBox = driver.find_element_by_xpath(xpathHEL)


	#SmallCapClickBox = driver.find_element_by_xpath(xpathSmallCap)


	#MidCapClickBox.click()

	#SmallCapClickBox.click()

	time.sleep(6.75)

	div = driver.find_element_by_id('searchSharesListOutput')

	tbody = div.find_element(By.TAG_NAME, 'tbody')
	tableRows = tbody.find_elements(By.TAG_NAME, 'tr')
	amountOfStock = len(tableRows)
	print("AmountOfStock = " + str(amountOfStock))
	file.write("AmountOfStock = " + str(amountOfStock) + '\n')
	file.write("Script started ")
	file.write(datetime.now().strftime("%H:%M:%S") + '\n' )
	#print("Script started: " + datetime.now().strftime("%H:%M:%S") + '\n')
	amountOfLinks = 0

	stockNames = []
	openingPrices = []
	lowestPrices = []
	highestPrices = []
	closingPrices = []
	totalVolumes = []

	for rows in tableRows:
		currentLink = rows.find_element_by_css_selector("td:nth-of-type(2)>a")
		amountOfLinks += 1
		link = currentLink.get_attribute('href')
		time.sleep(7)

		#print(stockName)

		driver2.get(link)
		#nameXpath = "//*[@id=\"shareInfoTop\"]/li[1]/h1/span"
		nameXpath = "/html/body/section/div/div/div/section/div[1]/article/div/div[2]/div[1]/ul[1]/li[1]/h1/span"
		nameElement = driver2.find_element_by_xpath(nameXpath)
		closingPriceElement = driver2.find_element_by_css_selector(".valueLatest")
		openingPriceElement = driver2.find_element_by_css_selector(".op")
		lowestPriceElement = driver2.find_element_by_css_selector(".lp")
		highestPriceElement = driver2.find_element_by_css_selector(".hp")
		totalVolumeElement = driver2.find_element_by_css_selector(".tv")
		time.sleep(2)
		stockNames.append(nameElement.text)
		openingPrices.append(openingPriceElement.text)
		lowestPrices.append(lowestPriceElement.text)
		highestPrices.append(highestPriceElement.text)
		closingPrices.append(closingPriceElement.text)
		totalVolumes.append(totalVolumeElement.text)

		'''
		print(nameElement.text)
		print("OpeningPrice: " + openingPriceElement.text)
		print("LowestPrice: " + lowestPriceElement.text)
		print("HighestPrice: " + highestPriceElement.text)
		print("closingPrice: " + closingPriceElement.text + '\n')
		file.write('\n' + nameElement.text)
		file.write("OpeningPrice: " + openingPriceElement.text)
		file.write("LowestPrice: " + lowestPriceElement.text)
		file.write("HighestPrice: " + highestPriceElement.text)
		file.write("ClosingPrice: " + closingPriceElement.text)
		file.write('\n')
		'''
		# create pandas DataFrame, which is a neat table of data.
	stockData = pd.DataFrame({'Stock': stockNames, 'Close': closingPrices, 'Open': openingPrices, 'Low': lowestPrices, 'High': highestPrices, 'Volume': totalVolumes})

	pd.set_option('display.max_rows', None)
	pd.set_option('display.max_columns', None)
	pd.set_option('display.width', None)
	pd.set_option('display.max_colwidth', -1)

	#create uniquefilename
	fileName = createUniqueFile()

	print(stockData)
	stockData.to_csv(fileName)

	print(str(amountOfLinks))
	#file.write("AmountOfLinks = " + str(amountOfLinks))
	file.write("Script ended: " + datetime.now().strftime("%H:%M:%S"))
	driver.quit()
	driver2.quit()
	file.close()
except Exception as e:
	logger.exception(e)
