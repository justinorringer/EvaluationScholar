from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
#import time

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

driver = webdriver.Firefox(options=fireFoxOptions)

def test_landing_page():
    driver.get("http://localhost/tasks")
    driver.find_element(By.ID, "toTasks").click()
    alert = driver.find_element(By.ID, "alert")
    #print(alert.text)

    assert "No tasks found. Upload or search for papers for an author to see scheduled tasks." in alert.text

    counter = driver.find_element(By.ID, "updateCounter").text

    #Test that counter label exists
    assert "Current Update Period: " in counter

    newCounter = driver.find_element(By.ID, "newCounterLabel").text

    assert "New Update Period (in Days):" in newCounter

    editBut = driver.find_element(By.ID, "editButton").text

    assert editBut == "Edit"



def test_timing_update():
    driver.get("http://localhost/tasks")
    counter = driver.find_element(By.ID, "updateCounter").text

    #Test that counter label exists
    assert "Current Update Period: " in counter

    driver.find_element(By.ID, "updatePeriod").send_keys("5")

    driver.find_element(By.ID, "editButton").click()

    counter = driver.find_element(By.ID, "updateCounter").text

    #Test that counter label exists with new value
    assert "Current Update Period: 5 days" in counter

    #This currently returns 50 by selenium, even though running this manually the page displays 5.
    #driver.find_element(By.ID, "updatePeriod").send_keys("0")

    #driver.find_element(By.ID, "editButton").click()

    #driver.refresh()

    #counter = driver.find_element(By.ID, "updateCounter").text

    #print(counter)

    #Test that counter label is not updated, zero is not valid
    #assert "Current Update Period: 5 days" in counter

#Testing specifically for new tasks may be tricky...

def runAll():
    try:
        print("Running test: Check static contents of landing page")
        test_landing_page()
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

    try:
        print("Running test: Check update of the update period label")
        test_timing_update()
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

#runAll()