import schedule
import time
from datetime import datetime
from Classes.Email import SendEmail
from database.db import user_collection
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def tracking():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (helps in some environments)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-logging")  # Disable logging

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        users_with_products = user_collection.find({
            "products": {"$exists": True, "$ne": []}  # Users with non-empty 'products' field
        })

        for user in users_with_products:
            user_email = user["email"]
            products = user.get("products", [])

            for product in products:
                driver.get(product["product_url"])

                # Fetch the current price
                price = driver.find_element(By.CSS_SELECTOR, "span.-b.-ubpt.-tal.-fs24.-prxs")
                new_price = int(price.text.split()[1].replace(",", ""))

                # Check if the price has dropped
                if new_price < product["current_price"]:
                    # Format the new price with commas
                    formatted_amount = "{:,}".format(new_price)

                    # Send email to notify the user
                    email_sender = SendEmail()
                    email_sender.send_price_drop_email(
                        recipient_email=user_email,
                        product_name=product["product_name"],
                        new_price=formatted_amount,
                        product_url=product["product_url"],
                        product_image_url=product["product_image_src"]
                    )

                    # Update the product with the new price
                    product["current_price"] = new_price

                # Update last_checked regardless of price change
                product["last_checked"] = datetime.now().isoformat()

            # Update the user's products in the database
            user_collection.update_one(
                {"email": user_email},
                {"$set": {"products": products}}
            )
    finally:
        driver.quit()


def schedule_tracking():
    # Schedule the tracking task to run every 4 hours
    schedule.every(4).hours.do(tracking)
    while True:
        schedule.run_pending()  # Run scheduled tasks
        time.sleep(1)  # Sleep to avoid high CPU usage
