import sys
import selenium
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import csv
import os


HOME = os.path.expanduser('~')
USERNAME = input("Please enter rapid7 username: ")
PASSWORD = input("Please enter rapid7 password: ")
SITE_ID = input("Please enter rapid7 site ID number: ")
FILE = input("Enter file name with extension: ")
#print(FILE)
input_file = []


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            input_file.append(os.path.join(root, name))
            print("File found. Starting automation process...")



find(FILE, HOME)
new_file = input_file.pop(0)
print(new_file)


driver = webdriver.Firefox()
driver.maximize_window()
type(driver)

# Login into rapid7
url = "https://rapid7.mlbcsi.com:3780/login.jsp"
driver.get(url)
driver.implicitly_wait(20)

userElem = driver.find_element_by_id("nexposeccusername")
userElem.send_keys(USERNAME)
passElem = driver.find_element_by_id("nexposeccpassword")
passElem.send_keys(PASSWORD)
loginElem = driver.find_element_by_id("login_button").click()


def create_blackout(date, hour, minute, duration):
    # goes to site that comes before blackout because it wont let you directly jump to the blackout edit page
    time.sleep(4)
    assetsElem = driver.find_element_by_xpath("/html/body/div[1]/div[2]/nav/div/ul/li[3]/a/span").click()
    time.sleep(5)
    sitesElem = driver.find_element_by_id("totalSites")
    driver.execute_script("arguments[0].click();", sitesElem)
    testsite = "https://rapid7.mlbcsi.com:3780/site.jsp?siteid=" + SITE_ID  # edit site id to the correct one as a string
    driver.get(testsite)
    driver.implicitly_wait(30)
    managesiteElem = driver.find_element_by_id("manage_site_button").click()
    scheduleElem = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[1]/ul/li[7]/div/label").click()
    blackoutElem = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div/div/ul/li[4]/a[1]").click()

    # input info here

    dateElem = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div/div/ng-include/div/form/fieldset/div[6]/div[1]/div[2]/input')
    driver.execute_script("arguments[0].removeAttribute('readonly')", dateElem)
    dateElem.clear()
    dateElem.send_keys(date)

    inputElement_HH = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div/div/ng-include/div/form/fieldset/div[6]/div[3]/div[2]/input[1]")
    inputElement_HH.send_keys(hour)

    inputElement_MM = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div/div/ng-include/div/form/fieldset/div[6]/div[3]/div[2]/input[2]")
    inputElement_MM.send_keys(minute)

    am_or_pm = Select(driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div/div/ng-include/div/form/fieldset/div[6]/div[3]/div[3]/div/select"))
    am_or_pm.select_by_index(0)

    inputDuration_HH = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div/div/ng-include/div/form/fieldset/div[12]/div[6]/input")
    inputDuration_HH.click()
    inputDuration_HH.send_keys(duration)


    save_blackout = driver.find_element_by_xpath('/html/body/div[3]/div[1]/div[2]/div[2]/div/div/div/div/ng-include/div/form/fieldset/div[17]/div[2]/button').click()



    # Save the configuration!!!!
    save_config = driver.find_element_by_id("btnScanConfigSave").click()



document = open(new_file)
with document as f:
    reader = csv.reader(f)
    your_list = list(reader)
    print(your_list)

for i in your_list:
    create_blackout(*i)