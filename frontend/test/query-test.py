from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


# This is a basic test to pull information from the 
# query page and assert the results


driver = webdriver.Firefox()
driver.get("http://localhost")
item = driver.find_element(By.ID, "PageTitle")
assert item.text == "EvaluationScholar"

authors = driver.find_element(By.ID, "authorForm").text
authors = authors.split("\n")

authors = Select(driver.find_element(By.ID, "authorForm"))

authors.select_by_visible_text("JP Ore")

driver.find_element(By.ID, "queryButton").click()

#Gets list of papers for JP Ore

papers = driver.find_element(By.ID, "paperTable").text
#Split into array to handle
papers = papers.split("\n")
#Ensure there are papers
assert len(papers) > 0

driver.close()