from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import random
from datetime import datetime
from Classes.Email import SendEmail
from selenium.webdriver.chrome.options import Options
from database.db import user_collection


class Tracking:
    def __init__(self, url, driver_path='chromedriver.exe'):
        self.driver_path = driver_path
        self.url = url
        # enable headless mode
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run Chrome in headless mode
        chrome_options.add_argument("--disable-gpu")  # Disable GPU (helps in some environments)
        chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better compatibility

        service = Service(self.driver_path)
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

        return {"product_name": product_name, "product_url": product_url, "current_price": price_text, "product_image_src": image_src}

    def start_tracking(self, user_email):
        # check the price every 4 hours
        while True:
            existing_user = user_collection.find_one({"email": user_email})

            if not existing_user:
                break

            products = existing_user.get('products', [])

            if not products:
                break

            for product in products:
                self.driver.get(product["product_url"])

                # Fetch the current price
                price = self.driver.find_element(By.CSS_SELECTOR, "span.-b.-ubpt.-tal.-fs24.-prxs")
                new_price = int(price.text.split()[1].replace(",", ""))

                # Check if the price has dropped
                if new_price < product["current_price"]:
                    # add the ',' when needed
                    formatted_amount = "{:,}".format(new_price)

                    # send email to notify the user
                    email_sender = SendEmail()
                    email_sender.send_price_drop_email(
                        recipient_email=existing_user["email"],
                        product_name=product['product_name'],
                        new_price=formatted_amount,
                        product_url=product['product_url'],
                        product_image_url=product['product_image_src'])

                    # Update the product with the new price
                    product["current_price"] = new_price

                # Update last_checked regardless of price change
                product["last_checked"] = datetime.now().isoformat()

                user_collection.update_one(
                    {"email": existing_user["email"]},
                    {"$set": {"products": products}}
                )

            # Sleep for 4 hours before checking prices again
            time.sleep(4 * 60 * 60)

    # def place_order_and_checkout(self):
    #     def human_like_delay(min_delay=1, max_delay=3):
    #         time.sleep(random.uniform(min_delay, max_delay))
    #     # select the add to cart button
    #     add_to_cart_btn = self.driver.find_element(By.CLASS_NAME, 'add.btn._prim.-pea._i.-fw')
    #
    #     # Random mouse movement before clicking
    #     action = ActionChains(self.driver)
    #     action.move_to_element(add_to_cart_btn).click()
    #     human_like_delay()
    #     action.perform()
    #
    #     # wait for the text "Product added successfully" to be present in Dom
    #     WebDriverWait(self.driver, 10).until(
    #         EC.text_to_be_present_in_element((By.CLASS_NAME, "cnt"), 'Product added successfully')
    #     )
    #
    #     # click the cart button
    #     cart_link = self.driver.find_element(By.CLASS_NAME, '-df.-i-ctr.-gy9.-hov-or5.-phs.-fs16')
    #     action.move_to_element(cart_link).click()
    #     human_like_delay()
    #     action.perform()
    #
    #     # click the checkout button
    #     checkout_link = self.driver.find_element(By.CLASS_NAME, '-fs0.-pas.-bt')
    #     action.move_to_element(checkout_link).click()
    #     human_like_delay()
    #     action.perform()

