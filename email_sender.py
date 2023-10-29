import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import pandas as pd


class SendEmail:

    def __init__(self):
        self.my_email = "YOUR_EMAIL"
        self.my_password = "YOUR EMAIL PASSWORD"
        self.recipient_list = []
        while True:
            self.new_email = input("Please enter your email address: ").lower().strip()
            confirm_email = input("Please confirm your email address: ").lower().strip()
            if self.new_email != confirm_email:
                print("Emails doesn't match!")
            else:
                break
        if self.new_email not in self.recipient_list:
            self.recipient_list.append(self.new_email)
            self.save_email_to_csv(self.recipient_list)
        else:
            print("You are already in the club")

    def send_email(self, receipient):
        # Create the email message
        message = MIMEMultipart()
        message["From"] = self.my_email
        message["To"] = receipient
        message["Subject"] = "Email Subject"

        # Add the email body
        body = "I have started executing"
        message.attach(MIMEText(body, "plain"))

        # Attach the file "flight_data.csv"
        with open("flights_data.csv", "rb") as file:
            attach = MIMEApplication(file.read(), _subtype="csv")
            attach.add_header("Content-Disposition", 'attachment; filename="flights_data.csv"')
            message.attach(attach)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.my_email, password=self.my_password)
            connection.sendmail(self.my_email, receipient, message.as_string())



    def save_email_to_csv(self, email_list):
        data_frame = pd.DataFrame({"emails":email_list})
        data_frame.to_csv("emails.csv", index=False)

