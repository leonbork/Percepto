from .base_page import BasePage

class ProductPage(BasePage):
    def has_price(self):
        return bool(self.driver.find_elements("class name", "product-price"))

    def is_price_text_size_correct(self):
        price_element = self.driver.find_element("class name", "product-price")
        return "1.8rem" in price_element.value_of_css_property("font-size")