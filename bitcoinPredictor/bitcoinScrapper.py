from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup as bs

driver = webdriver.Chrome()
driver.get('https://coinmarketcap.com/currencies/bitcoin/historical-data/')

dateList = []
highList = []
marketCap = []
driver.maximize_window()
time.sleep(5)
wait = WebDriverWait(driver, 20)

dates = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/span/button')
#driver.execute_script("arguments[0].scrollIntoView();", dates)
dates.click()

dateEl = '/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div[1]'
firstDateFound = 'December 2009'
firstDate = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div[1]')
leftArrow = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/button[1]')
body = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]')
while(firstDate.text != firstDateFound):
    leftArrow.click()
selection = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/div[1]/div[3]')
selection.click()
driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/div[1]/div/div/div[1]/div/div/div[2]/button[2]').click()

time.sleep(5)
loadElement = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[3]/div/div/p[1]/button')
driver.execute_script("arguments[0].scrollIntoView();", loadElement)
loadElement.click()
