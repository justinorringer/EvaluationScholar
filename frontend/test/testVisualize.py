from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback

#Webdriver setup
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)

def test_contents():
    driver.get("http://localhost")

    driver.find_element(By.ID, "toVisualize").click()

    title = driver.find_element(By.ID, "vizTitle").text
    assert title == "Visualize"

    boxplotBut = driver.find_element(By.ID, "simple-tab-0").text
    assert boxplotBut == "BOXPLOT"

    filter = driver.find_element(By.ID, "filter-select").text
    assert filter == "Authors"

def runAll():
    pass_fail=[0,0]

    try:
        print("Running Test: Check contents of Visualize page on boot")
        test_contents()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1
    driver.close()
    return pass_fail
