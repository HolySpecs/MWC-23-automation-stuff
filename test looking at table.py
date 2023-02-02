"""
Python Code that reads the names in the table in the mwc 2023 website

Nicholas Henryanto

Last Updated: 2/2/2023
"""

import time, csv, os.path
from selenium import webdriver
from selenium.webdriver.common.by import By

#the categories/markets
categoryNameList = ["5G","AGRITECH AND AGRIFOOD","APP/MOBILE SERVICES","ARTIFICIAL INTELLIGENCE","AUTOMOTIVE/TRANSPORT","BIG DATA/ANALYTICS","CLIMATE & ENVIRONMENT","CLOUD SERVICES","CONSULTANCY","CYBERSECURITY","DEVICE HARDWARE/SOFTWARE","DIGITAL IDENTITY/AUTHENTICATION","E-COMMERCE/DIGITAL COMMERCE","EDUCATION","ENTERPRISE & BUSINESS IT","ENTERPRISE SOFTWARE","FINTECH/FINANCE/INSURANCE SERVICES","GAMING","GOVERNMENT/PUBLIC POLICY","HEALTH/FITNESS/WELLBEING","IOT","MANUFACTURING AND INDUSTRY 4.0","MARKETING/ADVERTISING","MEDIA/CONTENT/ENTERTAINMENT","METAVERSE/VIRTUAL REALITY/AUGMENTED REALITY","MNO/MVNO","NETWORK INFRASTRUCTURE","NETWORK SECURITY","OSS/BSS","RETAIL/DISTRIBUTION CHANNELS","SATELLITE","SMART CITIES","SOFTWARE SERVICES","SUSTAINABLE DEVELOPMENT/SOCIAL INNOVATION","SYSTEMS INTEGRATION","USER EXPERIENCE","VENTURE CAPITAL/INVESTMENT/M&A","WEB3, CRYPTO AND NFTS"]

#set up the page and return the driver
def openPage():
    #open the browser
    driver = webdriver.Chrome(executable_path="chromedriver_win32\chromedriver.exe")
    #go to the website
    driver.get("https://www.mwcbarcelona.com/exhibitors")
    time.sleep(1)
    #find the accept cookies button and click it
    cookiesButton = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookiesButton.click()
    time.sleep(1)
    return driver

#go to the next page
def clickNextPage(driver):
    #find the next page button
    nextPageButton = driver.find_element(By.CSS_SELECTOR,"[aria-label='Next page']")
    #execute javascript code to find the element
    driver.execute_script("arguments[0].scrollIntoView(true);", nextPageButton)
    #wait for page to load
    time.sleep(1)
    #click the next page button
    nextPageButton.click()
    time.sleep(1)

#read what is on the page and return the exhibitors on the page
def readPage(driver):
    exhibitors = []
    #find the names of the exhibitors on the page
    pageItems = driver.find_elements(By.CLASS_NAME, "ais-Highlight-nonHighlighted")
    #add the exhibitor name to the exhibitors list
    for item in pageItems:
        exhibitors.append(item.text)
    return exhibitors

#save the names in an external file
def saveExhibitors(exhibitors, fileName):
    with open(fileName, 'w', encoding='utf-8-sig') as file:
        mywriter = csv.writer(file, quoting=csv.QUOTE_ALL)
        mywriter.writerow(exhibitors)

#click the categories in the page and return it
def getCategoryElementList(driver):
    return driver.find_elements(By.XPATH, '//section[1]/div/div/div/div/div[1]/div/div[3]/ul/li')

#click the category that you want and return the filename to save the exhibitors list
def clickCategory(category, categoryElementList, driver):
    #find the category
    currentCategory = None
    #check if the given category is in the list
    for item in categoryElementList:
        if category == item.text:
            currentCategory = item
            break
    #if the category couldn't be found
    if currentCategory == None:
        raise Exception("Error, current category is not working properly")
        return
    else:
        #Go to the category in the page
        driver.execute_script("arguments[0].scrollIntoView(true);", currentCategory)
        time.sleep(1)
        #click the category
        currentCategory.click()
        time.sleep(1)
        #make the filename
        if "/" in category:
            category = category.replace("/"," or ")
        fileName = category + " Exhibitors.csv"
        #save it in the results foder
        return os.path.join("./results/", fileName)
        print("Category Selected")
    pass

#function to get the atendees for a given category
def atendeeInCategory(category):
    #setup for reading and storing the exhibitors
    exhibitors = []
    driver = openPage()
    categoryElementList = getCategoryElementList(driver)
    fileName = clickCategory(category, categoryElementList, driver)
    time.sleep(1)

    #will continue reading the items and going to the next page until it can't
    try:
        while True:
            #store the exhibitors that are on the current page
            temp = readPage(driver)
            for item in temp:
                #add them to the exhibitors list
                exhibitors.append(item)
            #go to the next page
            clickNextPage(driver)
    except:
        pass
    #save exhibitors in external file
    saveExhibitors(exhibitors, fileName)
    #close the page
    driver.close()

#function to execute
def main():
    #go through all the categories
    for item in categoryNameList:
        atendeeInCategory(item)

main()