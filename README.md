# Python Selenium TerminalX Test Framework For Percepto

## 📌 Project Overview
This is a Selenium-based automated testing framework for the TerminalX website. It follows the Page Object Model (POM) pattern and uses `pytest` for test execution.

## 📂 Project Structure
```
selenium_terminalx/
│-- pages/
│   │-- __init__.py
│   │-- base_page.py
│   │-- login_page.py
│   │-- home_page.py
│   │-- product_page.py
│-- tests/
│   │-- __init__.py
│   │-- test_login.py
│   │-- test_search.py
│   │-- test_sorting.py
│   │-- test_product.py
│-- config.json
│-- requirements.txt
│-- README.md
```

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies
Ensure you have Python installed, then run:
```bash
pip install -r requirements.txt
```

### 2️⃣ Install WebDriver
This framework uses `webdriver-manager` to automatically handle ChromeDriver installation. No manual download is required.

### 3️⃣ Ensure `config.json` Exists
Create a `config.json` file in the project root and add your test user credentials:
```json
{
    "users": [
        {"username": "mail@mail.com", "password": "123"},
        {"username": "mail2@mail.com", "password": "456"}
    ]
}
```

### 4️⃣ Run Tests
Execute the test suite from the project root:
```bash
pytest tests/
```

To run a specific test file:
```bash
pytest tests/test_login.py
