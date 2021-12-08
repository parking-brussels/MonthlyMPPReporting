import random
import smtplib
import base64
import string
from typing import List
from bs4 import BeautifulSoup


class Mail:
    receiver: str
    text: str
    attachments: List[str]
    html: str
    sender: str = 'ict@parking.brussels'
    marker: str
    body: str = None

    def __init__(self, email: str, attachments: List[str], _body: str = None, _text: str = None):
        self.receiver = email
        self.attachments = attachments
        self.html = _body
        self.marker = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        if _text is not None:
            self.text = _text
        else:
            self.text = self.convertBodyToText(_body)

    def send(self):
        self.createHeader()
        self.addBody()
        for fileName in self.attachments:
            self.addFileToMail(fileName)
        # Add endmarker
        self.body += """--
"""
        try:
            smtpObj = smtplib.SMTP('relay.irisnet.be')
            smtpObj.sendmail(self.sender, self.receiver, self.body)
        except Exception as e:
            raise Exception("Error sending mail %s" % (str(e)))

    def createHeader(self):
        # if body is not empty header will not be at the beginning => raise exception
        if self.body is not None:
            raise Exception("Mail header build on top of existing body")

        self.body = """
From: %s
To: %s
Subject: 
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary= %s
--%s
""" % (self.sender, self.receiver, self.marker, self.marker)

    @staticmethod
    def convertBodyToText(HTMLtext: str):
        soup = BeautifulSoup(HTMLtext, features="html.parser")
        return soup.get_text('\n')

    def addFileToMail(self, _filename: str):
        file = open(_filename, "rb")
        encodedcontent = base64.b64encode(file.read())
        self.body += """
Content-Type: multipart/mixed; name=\"%s\"
Content-Transfer-Encoding:base64
Content-Disposition: attachment; filename=%s

%s
--%s""" % (_filename, _filename, encodedcontent, self.marker)

    def addBody(self):
        self.body += """
Content-Type: text/plain
Content-Transfer-Encoding:8bit

%s
--%s""" % (self.text, self.marker)
        if self.html is not None:
            self.body += """
Content-Type: text/html; charset=UTF-8


%s
--%s""" % (self.html, self.marker)
