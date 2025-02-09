from pages.base_page import BasePage


class LoginPage(BasePage):
    def login(self, username, password):
        self.driver.find_element("data-test-id", "qa-header-login-button").click()
        self.driver.find_element("id", "qa-login-email-input").send_keys(username)
        self.driver.find_element("id", "qa-login-password-input").send_keys(password)
        self.driver.find_element("data-test-id", "qa-login-submit").click()

    def is_logged_in(self):
        return "Logout" in self.driver.page_source