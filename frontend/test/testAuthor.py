from selenium import webdriver

from baseMethods import Baseline

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import traceback
import time

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
    authors = driver.find_element(By.ID, "combo-box-demo")

    authors.send_keys("John-Paul Ore")
    authors.send_keys(Keys.DOWN)
    authors.send_keys(Keys.RETURN)

    time.sleep(2)
    papers = driver.find_element(By.ID, "paperTableBody").text

    #print(papers)

    #Split papers into an array
    papers = papers.split("\n")

    #Check that the papers loaded
    assert len(papers) > 0

    #Check for a specific paper we know exists
    assert "Phriky-units: a lightweight, annotation-free physical unit inconsistency detection tool 2017 15" in papers


def sanity_check():
    try: 
        testingOre(driver)
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

    driver.close()

#sanity_check()

#driver.close()