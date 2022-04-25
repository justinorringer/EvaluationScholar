from selenium import webdriver

from baseMethods import Baseline

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.headless = True

driver = webdriver.Firefox(options=fireFoxOptions)

Baseline.setup_system(driver)

def sanity_check():
    try: 
        Baseline.testingOre(driver)
        print("Test: PASS")
    except:
        print("Test: FAIL")

sanity_check()

driver.close()