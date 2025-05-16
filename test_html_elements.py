from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import unittest
import os

class TestContacts(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(options=options)

    def test_contacts(self):
        driver = self.driver
        target_url = os.getenv("TARGET_URL", "http://10.48.10.127")
        driver.get(target_url)

        for i in range(10):
            name = f'Test Name {i}'
            phone = f'123-456-789{i}'
            address = f'{i} Example St, City, ST 1234{i}'

            page = driver.page_source
            self.assertIn(name, page, f"Missing name: {name}")
            self.assertIn(phone, page, f"Missing phone: {phone}")
            self.assertIn(address, page, f"Missing address: {address}")

        print("✔ All 10 sample contacts were successfully verified.")

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
