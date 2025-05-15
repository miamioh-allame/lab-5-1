from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest
import os

class TestContacts(unittest.TestCase):
    def setUp(self):
        # Setup headless Firefox browser
        firefox_options = Options()
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=firefox_options)

    def test_contact_page_loads(self):
        driver = self.driver
        target_url = os.getenv("TARGET_URL", "http://10.48.10.127")
        driver.get(target_url)
        self.assertIn("Contact List", driver.page_source)

    def test_input_fields_exist(self):
        driver = self.driver
        target_url = os.getenv("TARGET_URL", "http://10.48.10.127")
        driver.get(target_url)
        input_fields = driver.find_elements(By.TAG_NAME, "input")
        print(f"Found {len(input_fields)} input fields")
        self.assertGreater(len(input_fields), 0, "No input fields found.")

    def test_total_number_of_contacts(self):
        driver = self.driver
        target_url = os.getenv("TARGET_URL", "http://10.48.10.127")
        driver.get(target_url)
        contact_rows = driver.find_elements(By.XPATH, "//table//tr")[1:]  # skip header
        print(f"Found {len(contact_rows)} contact rows")
        self.assertGreater(len(contact_rows), 0, "No contact rows found.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
