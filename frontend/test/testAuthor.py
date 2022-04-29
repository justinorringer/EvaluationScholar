from selenium import webdriver
from baseMethods import Baseline
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import time

"""
This is a test file to create a webdriver and run tests speicifically on the Author page of
Evaluation Scholar, testing different aspects of the intended functionality.

Author: Gage Fringer
"""

#Webdriver setup
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)
Baseline.setup_system(driver)

"""
This method is a sanity check to ensure that the created author is referenced correctly.
"""
def testingOre(driver):
    print("Running test: Inspect created Author for papers")
    driver.get("http://localhost")

    #Search for Ore, navigate to his page
    authors = driver.find_element(By.ID, "combo-box-demo")
    authors.send_keys("John-Paul Ore")
    authors.send_keys(Keys.DOWN)
    authors.send_keys(Keys.RETURN)

    time.sleep(2)

    #Examine the papers he currently has (should have those from the test file)
    papers = driver.find_element(By.ID, "paperTableBody").text

    #Split papers into an array
    papers = papers.split("\n")

    #Check that the papers loaded
    assert len(papers) > 0

    #Check for a specific paper we know exists
    assert "Phriky-units: a lightweight, annotation-free physical unit inconsistency detection tool 2017 15" in papers

#Run the sanity test above with debug tracing output to console
def sanity_check():
    pass_fail=[0,0]
    try: 
        testingOre(driver)
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    driver.close()
    return pass_fail