# An interface to e-mail functionality

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailInterface:
    __logger = None
    __server = "smtp.mail.yahoo.com"
    __port = 587
    __user = "sanj19972001"
    __password = "oldemail123"
    __from = "sanj19972001@yahoo.com"
    __to = None
    __cc = None
    __rcpts = None
    __subject = None
    __msgText = None
    __msgType = None

    def set_logger(self, logger):
        self.__logger = logger

    def reset(self):
        self.__to = None
        self.__cc = None
        self.__rcpts = None
        self.__subject = None
        self.__msgText = None
        self.__msgType = None

    def set_recipients(self, to, cc=None):
        self.__to = to
        self.__cc = cc
        self.__rcpts = to.split(",")
        if cc:
            self.__rcpts += cc.split(",")

    def set_message(self, subject, text, msgtype="html"):
        self.__subject = subject
        self.__msgText = text
        self.__msgType = msgtype

    def send(self):
        message = MIMEMultipart()
        message["Subject"] = self.__subject
        message["From"] = self.__from
        message["To"] = self.__to
        if self.__cc:
            message["Cc"] = self.__cc

        part = MIMEText(self.__msgText, self.__msgType)
        message.attach(part)

        with smtplib.SMTP(self.__server, self.__port) as server:
            self.__logger.info(f"Connecting to {self.__server}:{self.__port}")
            server.starttls()
            server.login(self.__user, self.__password)
            self.__logger.info(f"Sending email to {self.__rcpts}")
            server.sendmail(self.__from, self.__rcpts, message.as_string())
