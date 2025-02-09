from selenium.webdriver.common.by import By

class ProductPage:
    PRODUCT_PRICE = (By.CSS_SELECTOR, "span.product-price")

    def __init__(self, driver):
        self.driver = driver

    def check_price_and_text_size(self):
        price_element = self.driver.find_element(*self.PRODUCT_PRICE)
        price_exists = price_element.is_displayed()
        text_size = self.driver.execute_script("return window.getComputedStyle(arguments[0]).fontSize;", price_element)
        return price_exists and text_size == "1.8rem"