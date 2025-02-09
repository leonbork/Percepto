import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SearchPage:
    SEARCH_INPUT = (By.NAME, "search")
    DROPDOWN_RESULTS = (By.CSS_SELECTOR, "ul.suggestions li")

    def __init__(self, driver):
        self.driver = driver

    def search(self, query):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        ).send_keys(query)
        time.sleep(2)

    def check_dropdown_results(self):
        results = self.driver.find_elements(*self.DROPDOWN_RESULTS)
        return all("hello kitty" in result.text.lower() for result in results)