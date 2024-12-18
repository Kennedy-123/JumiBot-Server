import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from flask import render_template

# Load the .env file
load_dotenv()


class SendEmail:
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.email_address = 'kennedyokolo222@gmail.com'
        self.email_password = os.getenv('EMAIL_PASSWORD')

    def send_price_drop_email(self, recipient_email, product_name, new_price, product_url, product_image_url):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                }}
                .container {{
                    margin: 20px;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .product-image {{
                    max-width: 100%;
                    height: auto;
                    margin-bottom: 20px;
                }}
                .button {{
                    display: inline-block;
                    margin-top: 20px;
                    padding: 10px 15px;
                    background-color: #007bff;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Price Drop Alert for {product_name}</h2>
                <img src="{product_image_url}" alt="Product Image" class="product-image">
                <p>The price of <strong>{product_name}</strong> has dropped!</p>
                <p>New Price: <strong>₦ {new_price}</strong></p>
                <p>Click the link below to view the product:</p>
                <a href="{product_url}" class="button">View Product</a>
            </div>
        </body>
        </html>
        """

        # Create the email message
        msg = MIMEMultipart("alternative")
        msg['From'] = self.email_address
        msg['To'] = recipient_email
        msg['Subject'] = f"Price Drop Alert: {product_name}"

        # Attach the HTML content
        msg.attach(MIMEText(html_content, "html"))

        try:
            # Send the email using SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
                # return True, "email sent"
                print('email sent')
        except Exception as e:
            # return False, f"Error sending email: {str(e)}"
            print(f'error: {e}')

    def send_welcome_email(self, user_email, user_name):
        html_content = render_template(
            'welcome_email_template.html',
            user_name=user_name,
        )
        # Create the email message
        msg = MIMEMultipart("alternative")
        msg['From'] = self.email_address
        msg['To'] = user_email
        msg['Subject'] = "Welcome to Autobot!"

        # Attach the HTML content
        msg.attach(MIMEText(html_content, "html"))

        # Send the email via the SMTP server
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.email_address, self.email_password)
                server.sendmail(
                    self.email_address,
                    user_email,
                    msg.as_string()
                )
                print(f"Welcome email successfully sent to {user_email}")
        except Exception as e:
            print(f"Failed to send email to {user_email}. Error: {e}")
