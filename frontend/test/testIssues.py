from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback

#Webdriver setup
fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True
driver = webdriver.Firefox(options=fireFoxOptions)

def test_contents():
    driver.get("http://localhost")

    driver.find_element(By.ID, "toIssues").click()

    title = driver.find_element(By.ID, "issuesTitle").text

    assert title == "Ambiguous Paper Issues"

    alert = driver.find_element(By.ID, "alert").text

    assert "No issues found!" in alert

def runAll():
    pass_fail=[0,0]
    try:
        print("Running Test: Check contents of Issues page on boot")
        test_contents()
        print("Test: PASS")
        pass_fail[0] += 1
    except:
        print("Test: FAIL")
        print(traceback.print_exc())
        pass_fail[1] += 1
    driver.close()
    return pass_fail
