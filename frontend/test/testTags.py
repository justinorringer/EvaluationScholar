from selenium import webdriver
from baseMethods import Baseline
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import traceback
import time

"""
This file holds tests related to specifically testing the functionality of the Tags page
of Evaluation Scholar to ensure it behaves as expected.

Author: Gage Fringer
"""

#Setup the webdriver
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)
Baseline.setup_system(driver)

#Test to check the contents of the page have loaded correctly
def test_contents():
    driver.get("http://localhost")
    driver.find_element(By.ID, "toTags").click()

    title = driver.find_element(By.ID, "tagTitle").text

    assert title == "Assign Tags to Authors"

#Test to make sure that creating a tag is successful
def test_create_tag():
    driver.get("http://localhost/tags")

    #Double check to remove the tag if it already exists, otherwise does nothing to the system state
    tags = driver.find_element(By.ID, "checkboxes-tags")
    tags.send_keys("Cool")
    tags.send_keys(Keys.DOWN)
    tags.send_keys(Keys.RETURN)
    driver.find_element(By.ID, "deleteButton").click()

    #give the page time to reload
    time.sleep(2)

    #Find and populate the text box to name the tag, then make it
    driver.find_element(By.ID, "tagBox").send_keys("Cool")
    driver.find_element(By.ID, "createButton").click()

    #Check to make sure that the tag success message is displayed
    message = driver.find_element(By.ID, "successspan").text
    assert "Tags Created Successfully" in message

#Test to check and make sure that assigning a tag to an author is successful
def test_assign_tag():
    driver.get("http://localhost/tags")

    #Ensure the tag exists
    driver.find_element(By.ID, "tagBox").send_keys("Cool")
    driver.find_element(By.ID, "createButton").click()

    #Gather JP Ore from the list of existing authors
    author = driver.find_element(By.ID, "checkboxes-authors")
    author.send_keys("John-Paul Ore")
    author.send_keys(Keys.DOWN)
    author.send_keys(Keys.RETURN)

    #Gather the created tag
    tags = driver.find_element(By.ID, "checkboxes-tags")
    tags.send_keys("Cool")
    tags.send_keys(Keys.DOWN)
    tags.send_keys(Keys.RETURN)

    #Attempt to assign the tag, and confirm this
    driver.find_element(By.ID, "assignButton").click()
    message = driver.find_element(By.ID, "successspan").text
    assert "Tags Assigned Successfully" in message

    #Navigate to JP Ore's page to ensure the tag is shown there
    driver.get("http://localhost")
    authors = driver.find_element(By.ID, "combo-box-demo")
    authors.send_keys("John-Paul Ore")
    authors.send_keys(Keys.DOWN)
    authors.send_keys(Keys.RETURN)
    time.sleep(2)
    element = driver.find_element(By.ID, "Cool")
    assert element

#Test to ensure that a tag is successfully unassigned from an author
def test_unassign_tag():
    driver.get("http://localhost/tags")

    #Ensure target tag exists
    driver.find_element(By.ID, "tagBox").send_keys("Cool")
    driver.find_element(By.ID, "createButton").click()

    #Select target author
    author = driver.find_element(By.ID, "checkboxes-authors")
    author.send_keys("John-Paul Ore")
    author.send_keys(Keys.DOWN)
    author.send_keys(Keys.RETURN)

    #Select target tag
    tags = driver.find_element(By.ID, "checkboxes-tags")
    tags.send_keys("Cool")
    tags.send_keys(Keys.DOWN)
    tags.send_keys(Keys.RETURN)

    #Attempt to unnasign tag. Since this is always run after the assign test, the tag should be there
    #if that test passes
    driver.find_element(By.ID, "unassignButton").click()
    message = driver.find_element(By.ID, "successspan").text
    assert "Tags Unassigned Successfully" in message

    #Check to make sure the change is reflected on JP Ore's page
    driver.get("http://localhost")
    authors = driver.find_element(By.ID, "combo-box-demo")
    authors.send_keys("John-Paul Ore")
    authors.send_keys(Keys.DOWN)
    authors.send_keys(Keys.RETURN)
    time.sleep(2)

    #Driver should throw an error, as it cannot find this tag on the page
    element = driver.find_element(By.ID, "Cool")
    assert element

#Deleting a tag currently causes an issue with the page reloading, and didn't want to have to deal with that

#function to aggregate running all tests for runAll file 
def runAll():
    pass_fail=[0,0]
    try:
        print("Running Test: Checking contents loaded correctly")
        test_contents()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    try:
        print("Running Test: Checking creation of a tag is successful")
        test_create_tag()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    try:
        print("Running Test: Checking assignment of tag to 'Ore' is successful")
        test_assign_tag()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    try:
        print("Running Test: Testing unassignment of tag from 'Ore'")
        test_unassign_tag()
        print("Test: FAIL (Exception not caught)")
        pass_fail[1] += 1
    except NoSuchElementException:
        #The driver should not have found the tag, and throws this error.
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    driver.close()
    return pass_fail
