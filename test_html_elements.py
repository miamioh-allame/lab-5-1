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
        firefox_options.add_argument("--headless")  # Run browser in headless mode
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_contacts(self):
        driver = self.driver
        target_url = os.getenv("TARGET_URL", "http://10.48.10.127")
        driver.get(target_url)

        # Expected real contacts
        real_contacts = [
            "Marie Alla",
            "John Smith",
            "Lisa Ray"
        ]

        # Check which contacts are found
        found = []
        for contact in real_contacts:
            if contact in driver.page_source:
                found.append(contact)
            else:
                print(f"❌ Expected contact '{contact}' not found in page source.")

        print(f"✅ Found contacts: {found}")

        # Ensure at least one real contact was found, else fail the test
        self.assertTrue(found, "❌ None of the expected real contacts were found.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
