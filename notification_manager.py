import smtplib
from data_manager import DataManager
from dotenv import load_dotenv
import os

load_dotenv()

my_email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
data_manager = DataManager()


class NotificationManager:

    def send_email(self, price, data, flight_link):
        email_data = data_manager.get_users_data()
        for email in email_data:
            with smtplib.SMTP("SMTP.mail.ru") as connection:  # According to your email it's changes
                connection.starttls()
                connection.login(user=my_email, password=password)
                try:
                    connection.sendmail(from_addr=my_email,
                                        to_addrs=email["email"],
                                        msg=f"Subject:{price}\n\n {data}\n{flight_link}".encode('utf-8'))

                except smtplib.SMTPDataError:
                    print(f"{email['email']} that's email doesn't exist!!!")
                    pass
