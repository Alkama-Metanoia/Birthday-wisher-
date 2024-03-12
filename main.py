from datetime import datetime
import pandas
import random
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

MY_EMAIL = "farhinanis14@gmail.com"
MY_PASSWORD = "quclovzcmyprsbdz"

try:
    connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
    connection.starttls()
    connection.login(MY_EMAIL, MY_PASSWORD)

    today = datetime.now()
    today_tuple = (today.month, today.day)

    data = pandas.read_csv("birthdays.csv")
    birthdays_dict = {(data_row.month, data_row.day): data_row for (index, data_row) in data.iterrows()}

    if today_tuple in birthdays_dict:
        birthday_person = birthdays_dict[today_tuple]
        file_path = f"letter_templates/letter_{random.randint(1,6)}.txt"
        print("File path:", file_path)
        print("Is file exist:", os.path.exists(file_path))
        with open(file_path) as letter_file:
            contents = letter_file.read()
            contents = contents.replace("[NAME]", birthday_person["name"])



        subject = "Happy Birthday!"
        body = f"{contents}".encode("utf-8")

        msg = MIMEMultipart()
        msg["From"] = formataddr(("Farhin Anis", MY_EMAIL))
        msg["To"] = birthday_person["email"]
        msg["Subject"] = subject

        msg.attach(MIMEText(contents, "plain"))

        connection.sendmail(from_addr=msg["From"],
                            to_addrs=birthday_person["email"],
                            msg=msg.as_string())

        connection.quit()
        print("Email sent successfully!")
except Exception as e:
    print("An error occurred:", str(e))
