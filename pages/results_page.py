import time
from selenium.webdriver.common.by import By

class ResultsPage:
    PRODUCT_PRICES = (By.CSS_SELECTOR, "span.product-price")
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "div.product-item")

    def __init__(self, driver):
        self.driver = driver

    def check_prices_sorted(self):
        prices = [float(price.text.replace("₪", "").replace(",", "")) for price in self.driver.find_elements(*self.PRODUCT_PRICES) if price.text]
        return prices == sorted(prices)

    def go_to_third_result(self):
        products = self.driver.find_elements(*self.PRODUCT_ITEMS)
        if len(products) >= 3:
            products[2].click()
            time.sleep(3)