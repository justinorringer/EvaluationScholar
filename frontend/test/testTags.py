from selenium import webdriver
from baseMethods import Baseline
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import traceback
import time


fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

driver = webdriver.Firefox(options=fireFoxOptions)

Baseline.setup_system(driver)

def test_contents():
    driver.get("http://localhost")
    driver.find_element(By.ID, "toTags").click()

    title = driver.find_element(By.ID, "tagTitle").text

    assert title == "Assign Tags to Authors"

def test_create_tag():
    driver.get("http://localhost/tags")

    tags = driver.find_element(By.ID, "checkboxes-tags")
    tags.send_keys("Cool")
    tags.send_keys(Keys.DOWN)
    tags.send_keys(Keys.RETURN)

    driver.find_element(By.ID, "deleteButton").click()

    #give the page time to reload
    time.sleep(2)

    driver.find_element(By.ID, "tagBox").send_keys("Cool")
    driver.find_element(By.ID, "createButton").click()

    message = driver.find_element(By.ID, "successspan").text

    #print(message)
    assert "Tags Created Successfully" in message

#successspan
def test_assign_tag():
    driver.get("http://localhost/tags")

    driver.find_element(By.ID, "tagBox").send_keys("Cool")
    driver.find_element(By.ID, "createButton").click()

    author = driver.find_element(By.ID, "checkboxes-authors")
    author.send_keys("John-Paul Ore")
    author.send_keys(Keys.DOWN)
    author.send_keys(Keys.RETURN)

    tags = driver.find_element(By.ID, "checkboxes-tags")
    tags.send_keys("Cool")
    tags.send_keys(Keys.DOWN)
    tags.send_keys(Keys.RETURN)

    driver.find_element(By.ID, "assignButton").click()

    message = driver.find_element(By.ID, "successspan").text

    #print(message)

    assert "Tags Assigned Successfully" in message

    driver.get("http://localhost")

    authors = driver.find_element(By.ID, "combo-box-demo")

    authors.send_keys("John-Paul Ore")
    authors.send_keys(Keys.DOWN)
    authors.send_keys(Keys.RETURN)

    time.sleep(2)

    element = driver.find_element(By.ID, "Cool")

    assert element


def test_unassign_tag():
    driver.get("http://localhost/tags")

    driver.find_element(By.ID, "tagBox").send_keys("Cool")
    driver.find_element(By.ID, "createButton").click()

    author = driver.find_element(By.ID, "checkboxes-authors")
    author.send_keys("John-Paul Ore")
    author.send_keys(Keys.DOWN)
    author.send_keys(Keys.RETURN)

    tags = driver.find_element(By.ID, "checkboxes-tags")
    tags.send_keys("Cool")
    tags.send_keys(Keys.DOWN)
    tags.send_keys(Keys.RETURN)

    driver.find_element(By.ID, "unassignButton").click()

    message = driver.find_element(By.ID, "successspan").text

    #print(message)

    assert "Tags Unassigned Successfully" in message

    driver.get("http://localhost")

    authors = driver.find_element(By.ID, "combo-box-demo")

    authors.send_keys("John-Paul Ore")
    authors.send_keys(Keys.DOWN)
    authors.send_keys(Keys.RETURN)

    time.sleep(2)

    element = driver.find_element(By.ID, "Cool")

    assert element

#Deleting a tag currently causes an issue with the page reloading, and didn't want to have to deal with that

def runAll():
    try:
        print("Running Test: Checking contents loaded correctly")
        test_contents()
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

    try:
        print("Running Test: Checking creation of a tag is successful")
        test_create_tag()
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

    try:
        print("Running Test: Checking assignment of tag to 'Ore' is successful")
        test_assign_tag()
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

    try:
        print("Running Test: Testing unassignment of tag from 'Ore'")
        test_unassign_tag()
        print("Test: FAIL (Exception not caught)")
    except NoSuchElementException:
        #The driver should not have found the tag, and throws this error.
        print("Test: PASS")
    except:
        print("Test: FAIL")
        print(traceback.print_exc())

    driver.close()
