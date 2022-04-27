from selenium import webdriver
from selenium.webdriver.common.by import By
import baseMethods
import traceback

#Webdriver setup
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)
baseMethods.Baseline.setup_system(driver)

def test_contents():
    driver.get("http://localhost")

    driver.find_element(By.ID, "toPapers").click()

    title = driver.find_element(By.ID, "paperTitle").text
    
    assert title == "Papers"

def test_ore_papers():
    driver.get("http://localhost/papers")

    driver.find_element(By.ID, "mui-1").send_keys("Assess")
    driver.find_element(By.ID, "searchButton").click()

    papers = driver.find_element(By.ID, "paperTableBody")

    #First page of Ore's papers should have 10
    paper10 = driver.find_element(By.ID, "paper10")
    assert paper10

    #There isn't an easy way to change pages to check the last 4 papers, but this way we can make sure at least 10 exist

    title = papers.find_element(By.ID, "name10").text
    assert title == "Assessing the type annotation burden"

    authors = papers.find_element(By.ID, "authors10")
    ore = papers.find_element(By.ID, "2").text
    assert ore == "John-Paul Ore"

    year = int(papers.find_element(By.ID, "year10").text)
    assert year == 2018

    citation10 = int(papers.find_element(By.ID, "citation10").text)
    #Can run this against the value we know, but the number could change in the future
    assert citation10 >= 15

#Running a delete paper test may cause problems if the tests are run more than once, since Ore doesn't get his papers repopulated

def runAll():
    pass_fail=[0, 0]

    try:
        print("Running Test: Check contents of Papers page on boot")
        test_contents()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1
    
    try:
        print("Running Test: Check contents of Papers for JP Ore")
        test_ore_papers()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1
    driver.close()
    return pass_fail