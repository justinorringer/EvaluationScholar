from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import os
import time

# This is a basic test file to setup the db and pull information from the 
class Baseline:
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.headless = True

    #driver = webdriver.Firefox(options=fireFoxOptions)
    """
    Method to ensure that the same data is loaded for each test in terms of authors.
    Uses test file to create John-Paul Ore with a set list of papers
    param: driver reference to a created webdriver for the test being run
    """
    def setup_system(driver):
        oreLoc = os.getcwd() + "\\files\\Ore.txt"
        driver.get("http://localhost")
        item = driver.find_element(By.ID, "PageTitle")
        assert item.text == "EvaluationScholar"

        #Check the list of authors to see if Ore Exists

        authors = driver.find_element(By.ID, "combo-box-demo")

        authors.send_keys("John-Paul Ore")
        authors.send_keys(Keys.DOWN)
        authors.send_keys(Keys.RETURN)

        time.sleep(2)

        currentLoc = driver.current_url
        print(currentLoc)

        if currentLoc != "http://localhost/":
            print("Have Ore")
            #authors = Select(driver.find_element(By.ID, "authorForm"))

            #authors.select_by_visible_text("John-Paul Ore")

            #driver.find_element(By.ID, "queryButton").click()

            #print(driver.find_element(By.ID, "paperTableBody").text)

            if driver.find_element(By.ID, "paperTableBody").text == "":
                driver.find_element(By.ID, "UploadPapers").click()
                print("Adding Papers")
                driver.find_element(By.ID, "myfile").send_keys(oreLoc)
                driver.find_element(By.ID, "uploadPapers").click() 
        else: 
            print("Don't have Ore, creating in the system")
            driver.find_element(By.ID, "toCreateAuthor").click()
            driver.find_element(By.ID, "authName").send_keys("John-Paul Ore")
            driver.find_element(By.ID, "searchButton").click()
            print("Performed Search")
            driver.implicitly_wait(5)
            #Grab the new author, hardcoded to Dr. Ore
            driver.find_element(By.ID, "John-Paul Ore+q7jnx5IAAAAJ").click()
            print("Navigated to page")
            driver.find_element(By.ID, "UploadPapers").click()
            print("Adding Papers")
            driver.find_element(By.ID, "myfile").send_keys(oreLoc)  
            driver.find_element(By.ID, "uploadPapers").click()      
            #Code to create an author


    #setup_system(driver)
    #testingOre(driver)

    #driver.close()

#    driver = webdriver.Firefox()
#    setup_system(driver)
#    driver.close()