from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
import time

"""
This test file is intended to test that the functionality of the "Create Author"
page behaves as expected by testing that the search returns 3 results (including a target result)
as well as options for a manual entry.

NOTE: Some of the API calling done for an author search is sometimes unsuccessful, causing tests to fail.
      To resolve, run the tests again.

Author: Gage Fringer
"""

#Set up webdriver
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)

#Method to test that searched author name exists and authors are provided
def test_author_creation_manual():
    driver.get("http://localhost")
    driver.find_element(By.ID, "toCreateAuthor").click()

    #Populate and run the search
    driver.find_element(By.ID, "authName").send_keys("John-Paul Ore")
    driver.find_element(By.ID, "searchButton").click()

    driver.implicitly_wait(10)

    #A button pops up on the page to create the author manually, check the text matches.
    nameCheck = driver.find_element(By.ID, "manualButton").text
    assert nameCheck == "Create 'John-Paul Ore'"

#Method to check the list of author options provided by the search returns expected info
def test_author_creation_list():
    driver.get("http://localhost")
    driver.find_element(By.ID, "toCreateAuthor").click()

    driver.find_element(By.ID, "authName").send_keys("John-Paul Ore")
    driver.find_element(By.ID, "searchButton").click()

    driver.implicitly_wait(10)

    #Three options are typically given, so all three are tested below

    JP1 = driver.find_element(By.ID, "John Alvarez or John Paul Alvarez+qnS2yEYAAAAJ").text

    assert "John Alvarez or John Paul Alvarez" in JP1
    assert "monash university" in JP1

    JP2 = driver.find_element(By.ID, "John-Paul Ore+q7jnx5IAAAAJ").text

    assert "John-Paul Ore" in JP2
    assert "North Carolina State University" in JP2

    JP3 = driver.find_element(By.ID, "John Paul Bigouette+vLnv7GAAAAAJ").text

    assert "John Paul Bigouette" in JP3
    assert "Oregon State University" in JP3
    
#Method to test an author that does not exist on Google Scholar, check that our system acknowledges that
def test_fake_author():
    driver.get("http://localhost")
    driver.find_element(By.ID, "toCreateAuthor").click()

    driver.find_element(By.ID, "authName").send_keys("Gage Fringer")
    driver.find_element(By.ID, "searchButton").click()

    driver.implicitly_wait(10)

    nameCheck = driver.find_element(By.ID, "manualOnlyButton").text

    assert nameCheck == "Create 'Gage Fringer' Anyway"

    nameCheck = driver.find_element(By.ID, "noresults").text

    assert "No results for this input, please try again." in nameCheck

#Method to run all tests and provide debugging in the event of a failure.
def run_tests():
    pass_fail=[0,0]

    try:
        print("Running test: Test to check results for 'John-Paul Ore'")
        test_author_creation_list()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    try:
        print("Running test: Ensure Manual Creation button has correct text")
        test_author_creation_manual()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1

    try:
        print("Running test: Search for nonexistent author (Gage Fringer)")
        test_fake_author()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1
    driver.close()
    return pass_fail