import os
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TestContacts(unittest.TestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(os.getenv("TARGET_URL", "http://10.48.10.127"))

    def test_real_contacts_present(self):
        driver = self.driver
        real_names = ["Marie Alla", "Daniel Kim", "Linda Tran", "Omar Farah", "Natalie Cruz"]
        for name in real_names:
            self.assertIn(name, driver.page_source, f"Contact {name} not found on the page")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
