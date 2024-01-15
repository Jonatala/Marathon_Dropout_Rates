import time
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

chrome_options = Options()
chrome_driver_path = "C:/Users/User2/Desktop/PGMP/chrome-win64"

# prefs = {"profile.managed_default_content_settings.images": 2}
# chrome_options.add_experimental_option("prefs", prefs)

chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)


expwait = WebDriverWait(driver, 10, ignored_exceptions=[Exception])
# website = 'https://www.manchestermarathon.co.uk/event-info/results/'
#website = 'https://results.sporthive.com/events/7039548795219704576/races/485067' # 2023
#website = 'https://results.sporthive.com/events/6908056816784834560/races/481319' # 2022

#website = 'https://results.sporthive.com/events/6850803266164094208/races/479767' #2021

website = 'https://results.sporthive.com/events/6488812689306147584/races/450756'   #2019

#website = 'https://results.sporthive.com/events/6908056816784834560/races/481540'

driver.get(website)
driver.maximize_window()
cookies_button = driver.find_element(By.CSS_SELECTOR,
                                     'body > div.cc-window.cc-banner.cc-type-opt-out.cc-theme-block.cc-bottom.cc-color-override-1747423907 > div > a.cc-btn.cc-dismiss')
cookies_button.click()

NextButtonDisabled = False

POS = []
NAME = []
BIB = []
M_F = []
TEAM_CLUB = []
CATEGORY = []
CHIP_TIME = []

while not NextButtonDisabled:
    time.sleep(1)
    table_data = driver.find_elements(By.XPATH,'.//tr')

    for data in table_data:
        try:
            POS.append(data.find_element(By.CSS_SELECTOR, 'td.col-is-pos').text)
            NAME.append(data.find_element(By.CSS_SELECTOR, 'td.col-is-name > p').text)
            BIB.append(data.find_element(By.CSS_SELECTOR, 'td.col-is-bib.color-grey-light.is-narrow.ng-binding.ng-scope').text)
            M_F.append(
                data.find_element(By.CSS_SELECTOR, 'td:nth-child(5)').text)
            TEAM_CLUB.append(data.find_element(By.CSS_SELECTOR, 'td.color-grey-light.is-wide.col-is-team > a').text)
            CATEGORY.append(data.find_element(By.CSS_SELECTOR, 'td:nth-child(10) > p').text)
            CHIP_TIME.append(data.find_element(By.CSS_SELECTOR, 'td.col-is-time.is-narrow.ng-scope > span').text)
        except Exception as e:
            print(f"Error: {e}")
            #print(f"Data: {data.text}")
            # Add more debug prints to identify the issue

    css_next_button = expwait.until(EC.presence_of_element_located((By.XPATH, '//a[text()="»"]/parent::li')))

    next_class = css_next_button.get_attribute('class')

    if "disabled" in next_class:
        NextButtonDisabled = True
    else:
        time.sleep(1)
        driver.find_element(By.XPATH, '//li[@class="ng-scope"]/child::a[text()="»"]').click()

driver.quit()



# Print lengths of lists for debugging
print(f"POS: {len(POS)}")
print(f"NAME: {len(NAME)}")
print(f"BIB: {len(BIB)}")
print(f"M_F: {len(M_F)}")
print(f"TEAM_CLUB: {len(TEAM_CLUB)}")
print(f"CATEGORY: {len(CATEGORY)}")
print(f"CHIP_TIME: {len(CHIP_TIME)}")


Marathon = {'POS': POS, 'NAME': NAME, 'BIB': BIB, 'M_F': M_F, 'TEAM_CLUB': TEAM_CLUB, 'CATEGORY': CATEGORY, 'CHIP_TIME': CHIP_TIME}
marathonJson = json.dumps(Marathon, indent=4)
# Specify the file path where you want to save the JSON file
json_file_path = '2019_Manchester_Marathon.json'
with open(json_file_path, 'w') as json_file:
    json_file.write(marathonJson)

