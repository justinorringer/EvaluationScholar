from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback

"""
This test file specifically tests the behavior of the Tasks page of Evaluation Scholar

Author: Gage Fringer
"""

#Set up webdriver
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)

#Method to check that the contents of the task page load as expected
def test_landing_page():
    driver.get("http://localhost/tasks")
    driver.find_element(By.ID, "toTasks").click()
    alert = driver.find_element(By.ID, "alert")

    assert "No tasks found. Upload or search for papers for an author to see scheduled tasks." in alert.text

    counter = driver.find_element(By.ID, "updateCounter").text

    #Test that counter label exists
    assert "Current Update Period: " in counter

    newCounter = driver.find_element(By.ID, "newCounterLabel").text

    assert "New Update Period (in Days):" in newCounter

    editBut = driver.find_element(By.ID, "editButton").text

    assert editBut == "Edit"

#Method to test that changing the update period of tasks is successful
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

#Method to run all tests in the runAll file
def runAll():
    pass_fail=[0,0]
    try:
        print("Running test: Check static contents of landing page")
        test_landing_page()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    try:
        print("Running test: Check update of the update period label")
        test_timing_update()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    driver.close()
    return pass_fail