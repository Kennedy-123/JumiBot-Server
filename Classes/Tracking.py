from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile


class Tracking:
    def __init__(self, url):
        self.url = url
        # enable headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU (helps in some environments)
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better compatibility
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Use a unique temporary directory for user data (to avoid conflicts)
        user_data_dir = tempfile.TemporaryDirectory()  # Automatically cleaned up
        chrome_options.add_argument(f"--user-data-dir={user_data_dir.name}")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def load_webpage(self):
        self.driver.get(self.url)

    def get_product_details(self):
        # get the product price
        price = self.driver.find_element(By.CSS_SELECTOR, "span.-b.-ubpt.-tal.-fs24.-prxs")
        price_text = int(price.text.split()[1].replace(",", ""))

        # get the product name
        product = self.driver.find_element(By.CLASS_NAME, "-fs20.-pts.-pbxs")
        product_name = product.text

        # get the product url
        product_url = self.driver.current_url

        image = self.driver.find_element(By.CLASS_NAME, '-fw.-fh')

        # Wait for the 'src' attribute to update to a valid URL
        WebDriverWait(self.driver, 10).until(lambda d: image.get_attribute("src").startswith("http"))

        # get the src
        image_src = image.get_attribute("src")

        return {"product_name": product_name, "product_url": product_url, "current_price": price_text,
                "product_image_src": image_src}
