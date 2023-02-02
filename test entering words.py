import csv, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#import the exhibitors from the exhibitors file
atendee = []
final = []
with open("mwc 2022 exhibitors.csv", 'r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    for row in reader:
        atendee.append(row)
temp = []
for i in range(0, len(atendee)):
    temp.append(atendee[i][0].split(' '))
print(temp[0][0])

#import the categories from the catagories file
catagories = []
with open("product catagories.csv", 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        catagories.append(row)

#function to check if the past attendee is coming this year
def checkCases(startNum, result):
    index = startNum
    try:
        #go through the list of atendees starting from startNum pos
        for item in atendee[startNum:]:
            index = atendee.index(item)
            #find the input box for searching the exhibitors
            inputElement = browser.find_element(By.TAG_NAME, "INPUT")
            #enter the exhibitor name
            if (len(temp[index][0]) <= 5):
                inputElement.send_keys(atendee[index])
            else:
                inputElement.send_keys(temp[index][0])
            time.sleep(0.15)
            #check if the page says No Result for the searched item
            checkEmpty = browser.page_source 
            if not ("No Result" in checkEmpty):
                result.append(item[0])
            #delete the search bar
            inputElement.send_keys(Keys.CONTROL, "a")
            inputElement.send_keys(Keys.BACKSPACE)
    except Exception as e:
        #print the error and return the last checked name if browser crashed
        print(e)
        return index

startPoint = 0
part = 1
try:
    #while there are still items in the atendees list
    while startPoint != None:
        result = []
        #open the browser, go to the website and accept the cookies
        browser = webdriver.Chrome(executable_path="chromedriver_win32\chromedriver.exe")
        browser.get("https://www.mwcbarcelona.com/exhibitors")
        time.sleep(1)
        cookiesButton = browser.find_element(By.ID, "onetrust-accept-btn-handler")
        cookiesButton.click()

        #start searching
        startPoint = checkCases(startPoint, result)
        #if the browser is being weird, close it
        browser.close()
        for item in result:
            final.append(item)

        """
        #add the confirmed names in a new file
        filename = "updatedExhibiteesPart" + str(part) + ".csv"
        part += 1
        with open(filename, "w", encoding='utf-8-sig') as file:
            mywriter = csv.writer(file, quoting=csv.QUOTE_ALL)

            mywriter.writerow(result)
        """
except Exception as e:
    print(e)

with open("updatedExhibiters.csv", "w", encoding='utf-8-sig') as file:
    mywriter = csv.writer(file, quoting=csv.QUOTE_ALL)
    mywriter.writerow(final)
