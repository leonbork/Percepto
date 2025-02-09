import json
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ------------------------------
# BasePage: common functionality
# ------------------------------
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Adjust wait timeout if needed
        self.wait = WebDriverWait(driver, 15)


# ------------------------------
# HomePage: actions on the home page
# ------------------------------
class HomePage(BasePage):
    URL = "https://www.terminalx.com/"

    def go_to_homepage(self):
        self.driver.get(self.URL)

    def click_login(self):
        # Assuming a "Login" link exists in the header.
        # Adjust the locator as needed.
        login_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Login"))
        )
        login_link.click()

    def search(self, phrase):
        # Adjust the locator for the search input if needed.
        # For example, using a CSS class 'search-input' or placeholder text.
        search_input = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input.search-input"))
        )
        search_input.clear()
        search_input.send_keys(phrase)
        # Wait briefly for the dropdown to populate
        time.sleep(2)


# ------------------------------
# LoginPage: actions on the login page
# ------------------------------
class LoginPage(BasePage):
    def login(self, username, password):
        # Adjust selectors according to the actual login page.
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        email_field.clear()
        email_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)

        # Assuming the login button is of type submit.
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        login_button.click()


# ------------------------------
# SearchResultsPage: actions on the search results dropdown
# ------------------------------
class SearchResultsPage(BasePage):
    def get_dropdown_results(self):
        # Adjust the container selector according to the site’s HTML.
        dropdown = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".search-dropdown"))
        )
        # Assuming each result is a list item <li>
        results = dropdown.find_elements(By.CSS_SELECTOR, "li")
        return results

    def get_product_prices(self):
        results = self.get_dropdown_results()
        prices = []
        for result in results:
            # Assume the price element is within the result and has a class "price"
            try:
                price_elem = result.find_element(By.CSS_SELECTOR, ".price")
                # Remove currency symbols and commas; adjust if needed.
                price_text = price_elem.text.strip().replace('$', '').replace(',', '')
                price_value = float(price_text)
                prices.append(price_value)
            except Exception as e:
                print("Could not parse price from result:", result.text)
                raise e
        return prices

    def click_result(self, index):
        results = self.get_dropdown_results()
        if index < len(results):
            results[index].click()
        else:
            raise Exception("Requested result index ({}) is out of range.".format(index))


# ------------------------------
# ProductPage: actions on the product detail page
# ------------------------------
class ProductPage(BasePage):
    def get_price_element(self):
        # Adjust the selector to match the product price element.
        price_elem = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".product-price"))
        )
        return price_elem

    def verify_price_text_size(self, expected_size="1.8rem"):
        price_elem = self.get_price_element()
        font_size = price_elem.value_of_css_property("font-size")
        # Depending on browser, computed font-size may be in pixels.
        # Here we compare directly to the expected value.
        print("Found font-size:", font_size)
        return font_size == expected_size


# ------------------------------
# Main test execution
# ------------------------------
def main():
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        # Instantiate HomePage and navigate to TerminalX
        home_page = HomePage(driver)
        home_page.go_to_homepage()
        print("Navigated to TerminalX homepage.")

        # Click on the Login link/button
        home_page.click_login()
        print("Clicked on Login.")

        # Instantiate LoginPage
        login_page = LoginPage(driver)

        # Load user credentials from the JSON file
        with open("../credentials.json", "r") as f:
            users = json.load(f)
        # Choose a random user from the list
        user = random.choice(users)
        print("Logging in with user:", user["username"])

        # Perform login
        login_page.login(user["username"], user["password"])
        print("Login submitted.")

        # Optionally, wait/check for an element that confirms login was successful.
        time.sleep(3)  # Adjust waiting as necessary

        # Perform a search for the phrase "hello"
        home_page.search("hello")
        print("Performed search for 'hello'.")

        # Instantiate SearchResultsPage and validate the dropdown
        search_results_page = SearchResultsPage(driver)
        results = search_results_page.get_dropdown_results()
        if not results:
            raise Exception("No dropdown results found.")

        # Check that every dropdown result contains the phrase "hello kitty"
        for idx, result in enumerate(results):
            result_text = result.text.lower()
            if "hello kitty" not in result_text:
                raise Exception(
                    "Dropdown result {} does not contain 'hello kitty': '{}'".format(idx + 1, result.text)
                )
            print("Dropdown result {} contains 'hello kitty': '{}'".format(idx + 1, result.text))
        print("All dropdown results contain 'hello kitty'.")

        # Check if the products are ordered ascending by price
        prices = search_results_page.get_product_prices()
        if prices != sorted(prices):
            raise Exception("Product prices are not in ascending order: {}".format(prices))
        print("Product prices are in ascending order:", prices)

        # Click on the third search result (index 2)
        search_results_page.click_result(2)
        print("Clicked on the third search result.")

        # Now on the product page, check that a price element exists
        product_page = ProductPage(driver)
        price_element = product_page.get_price_element()
        if not price_element:
            raise Exception("Price element not found on the product page.")
        print("Price element found on product page.")

        # Verify that the text size of the price is 1.8rem
        if not product_page.verify_price_text_size("1.8rem"):
            actual_size = price_element.value_of_css_property("font-size")
            raise Exception("Price element font-size is {}, expected 1.8rem.".format(actual_size))
        print("Price element font-size is 1.8rem as expected.")

        print("All tests passed successfully.")

    except Exception as e:
        print("Test failed:", str(e))
    finally:
        # Clean up and close the browser
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    main()