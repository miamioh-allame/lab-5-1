from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest
import os

class TestContacts(unittest.TestCase):
    def setUp(self):
        # Setup Firefox options
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_contacts(self):
    driver = self.driver
    driver.get("http://10.48.10.127")

    # Verify real contacts exist
    real_contacts = [
        "Marie Alla",
        "John Smith",
        "Lisa Ray"
    ]

    for contact in real_contacts:
        assert contact in driver.page_source, f"Expected contact '{contact}' not found."

    print("All real contacts successfully verified.")


    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
