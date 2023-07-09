from datetime import datetime
import os
import smtplib
from email.message import EmailMessage


class NotificationManager:
    def __init__(self):
        self.email_address = os.environ['email_address']
        self.smtp_password = os.environ['smtp_password']
        self.smtp_address = "smtp.gmail.com"
        self.smtp_port = 587
        self.email_body = ""

    def send_email(self, flight_details):
        departure_time_epoch = flight_details["data"][0]["route"][0]["dTimeUTC"]
        departure_time = datetime.fromtimestamp(departure_time_epoch)

        return_time_epoch = flight_details["data"][0]["route"][1]["aTimeUTC"]
        return_time = datetime.fromtimestamp(return_time_epoch)

        self.email_body = f"Cheap flight from {flight_details['data'][0]['route'][0]['cityFrom']} " \
                          f"to {flight_details['data'][0]['route'][0]['cityTo']}\n\n" \
                          f"Departure date: {departure_time}\n" \
                          f"Return date: {return_time}\n" \
                          f"Stay duration {flight_details['data'][0]['nightsInDest']}\n" \
                          f"Price: {flight_details['data'][0]['price']}"

        with smtplib.SMTP(self.smtp_address, self.smtp_port) as connection:
            connection.starttls()
            connection.login(self.email_address, self.smtp_password)

            msg = EmailMessage()
            msg['Subject'] = f"Cheap flight from {flight_details['data'][0]['route'][0]['cityFrom']} " \
                             f"to {flight_details['data'][0]['route'][0]['cityTo']}."
            msg['From'] = self.email_address
            msg['To'] = self.email_address
            msg.set_content(self.email_body)
            #
            connection.send_message(msg)
