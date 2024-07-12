#!/usr/bin/env python3
"""this model for sending an email using Gmail"""
from smtplib import SMTP
from os import getenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

DOMAIN_NAME = "http://localhost:5000"
EMAIL = getenv("EMAIL_USER", "")
PWD = getenv("EMAIL_PWD", "")


class SendEmail:
    """define class Email"""

    def __init__(self) -> None:
        """create in connect to Email"""
        self.connect = SMTP('smtp.gmail.com', 587)
        self.connect.starttls()
        self.connect.login(EMAIL, PWD)

    def sendEmail(self, receiver, content):
        """SendEmail"""
        self.connect.sendmail(EMAIL, receiver, content.as_string())
        # self.connect.quit()

    @staticmethod
    def signUp(full_name, receiver):
        """create content Welcoming an user signUp"""
        html = f"""
<html>
<head></head>
<body>
    <p>Dear <b>{full_name}</b>,</p>
    <p>We are thrilled to welcome you to BioMorocco, your go-to destination for the finest bio products in Morocco!</p>
    <p>At BioMorocco, we are committed to providing you with the highest quality organic products, from our renowned argan oil to a wide range of other natural goods. We believe in the power of nature and sustainability, and we're excited to have you join our community.</p>
    <p>Here are some key features you can enjoy as a member of BioMorocco:</p>
    <ul>
        <li><b>Exclusive Offers:</b> Be the first to know about our special promotions and discounts.</li>
        <li><b>Personalized Recommendations:</b> Receive tailored product suggestions based on your preferences.</li>
        <li><b>Fast and Secure Checkout:</b> Experience a seamless and secure shopping process.</li>
        <li><b>Customer Support:</b> Our dedicated support team is here to assist you with any inquiries or issues.</li>
        <li><b>Loyalty Program:</b> Earn points with every purchase and redeem them for discounts on future orders.</li>
    </ul>
    <p><b>Get Started:</b></p>
    <ul>
        <li><b>Explore Our Products:</b> Visit our <a href="{DOMAIN_NAME}">website</a> to discover our full range of bio products.</li>
        <li><b>Update Your Profile:</b> Complete your profile to help us serve you better.</li>
        <li><b>Follow Us on Social Media:</b> Stay connected and get the latest updates by following us on <a href="https://www.facebook.com/biomorocco">Facebook</a>, <a href="https://www.instagram.com/biomorocco">Instagram</a>, and <a href="https://www.twitter.com/biomorocco">Twitter</a>.</li>
    </ul>
    <p>If you have any questions or need assistance, feel free to reach out to us at <a href="mailto:{EMAIL}">{EMAIL}</a> or call us at <b>+21200000000</b>. We're here to help!</p>
    <p>Once again, welcome to the BioMorocco family. We look forward to providing you with the best in organic and natural products.</p>
    <p>Best Regards,</p>
    <p>The BioMorocco Team</p>
</body>
</html>
"""

        # Create the MIMEText objects for the email
        message = MIMEMultipart("alternative")
        message["Subject"] = "Welcome to BioMorocco"
        message["From"] = EMAIL
        message["To"] = receiver

        # Attach the HTML content to the email
        html_part = MIMEText(html, "html")
        message.attach(html_part)
        return message

    @staticmethod
    def create_content_for_forget_Password(full_name, receiver, token):
        """create content Welcoming an user signUp"""
        html = f"""
<html>
<head></head>
<body>
    <p>Dear <b>{full_name}</b>,</p>
    <p>We received a request to reset your password for your BioMorocco account. To ensure the security of your account, please use the verification code below to reset your password.</p>
    <p><b>Your Password Reset Code: {token}</b></p>
    <p><i>Please note, this code is only valid for 2 minute. If you do not use this code within the next 1 minute, you will need to request a new password reset.</i></p>
    <p><b>To reset your password:</b></p>
    <ol>
        <li>Go to the <a href="{DOMAIN_NAME}/reset-password">Password Reset Page</a>.</li>
        <li>Enter the verification code: <b>{token}</b></li>
        <li>Follow the instructions to create a new password.</li>
    </ol>
    <p>If you did not request a password reset, please ignore this email. Your account security is important to us, and no changes will be made without your verification code.</p>
    <p>For any further assistance, please contact our support team at <a href="mailto:support@biomorocco.com">support@biomorocco.com</a> or call us at [phone number].</p>
    <p>Thank you for being a part of BioMorocco.</p>
    <p>Best Regards,<br>The BioMorocco Team</p>
</body>
</html>
"""
        message = MIMEMultipart("alternative")
        message["Subject"] = "BioMorocco Password Reset Request"
        message["From"] = EMAIL
        message["To"] = receiver

        html_part = MIMEText(html, "html")
        message.attach(html_part)
        return message

    @staticmethod
    def create_content_for_new_order(owner, products, customer):
        """create content Welcoming an user signUp"""
        html_ordered_products = "<table border='1'><tr><th>Product</th><th>Quantity</th><th>Price</th></tr>"
        total = 0
        for product, quantity, total_price in products:
            html_ordered_products += f"<tr><td>{product.name}</td><td>{quantity}</td><td>{total_price} $</td></tr>"
            total += total_price
        html_ordered_products += "</table>"

        html = f"""
<html>
<head></head>
<body>
    <p>Dear <b>{owner.first_name} {owner.last_name}</b>,</p>
    <p>You have received a new order from a customer. Here are the details:</p>
    <ul>
        <li><p><b>Customer Name:</b> {customer.first_name} {customer.last_name}</p></li>
        <li><p><b>Phone Number:</b> {customer.phone}</p></li>
        <li><p><b>Email:</b> <a href="mailto:{customer.email}">{customer.email}</a></p></li>
        <li><p><b>Country:</b> {customer.country}</p></li>
        <li><p><b>State:</b> {customer.state}</p></li>
        <li><p><b>City:</b> {customer.city}</p></li>
        <li><p><b>Address:</b> {customer.address}</p></li>
    </ul>
    <p><b>Order Details:</b></p>
    {html_ordered_products}
    <p><b>total price:</b> {total} $.</p>
    <p>Please process this order as soon as possible to ensure timely delivery to the customer.</p>
    <p>If you need any assistance, feel free to reach out to us at <a href="mailto:support@biomorocco.com">support@biomorocco.com</a>.</p>
    <p>Best Regards,</p>
    <p>The BioMorocco Team</p>
</body>
</html>
"""
        message = MIMEMultipart("alternative")
        message["Subject"] = "New Order Received"
        message["From"] = EMAIL
        message["To"] = owner.email

        # Attach the HTML content to the email
        html_part_new_order = MIMEText(html, "html")
        message.attach(html_part_new_order)
        return message

    @staticmethod
    def create_content_for_low_stock_dedicated(owner, product):
        """create content Welcoming an user signUp"""
        html = f"""
<html>
<head></head>
<body>
    <p>Dear <b>{owner.first_name} {owner.last_name}</b>,</p>
    <p>We wanted to inform you that the stock level for the following product is running low:</p>
    <p><b>Product:</b> {product.name}</p>
    <p><b>Current Stock:</b> {product.stock} units</p>
    <p>Please check your inventory and restock this product to ensure continuous availability for your customers.</p>
    <p>If you need any assistance, feel free to reach out to us at <a href="mailto:support@biomorocco.com">support@biomorocco.com</a>.</p>
    <p>Best Regards,</p>
    <p>The BioMorocco Team</p>
</body>
</html>
"""
        message = MIMEMultipart("alternative")
        message["Subject"] = "Low Stock Alert: Action Required"
        message["From"] = EMAIL
        message["To"] = owner.email

        # Attach the HTML content to the email
        html_part_new_order = MIMEText(html, "html")
        message.attach(html_part_new_order)
        return message
