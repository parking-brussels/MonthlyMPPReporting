
import smtplib
from os.path import basename
from typing import List
from bs4 import BeautifulSoup
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid



class Mail:
    text: str
    attachments: List[str]
    message: EmailMessage
    html: str
    marker: str


    def __init__(self,
                 _email: str,
                 _attachments: List[str],
                 _body: str = None,
                 _text: str = None,
                 _subject: str = None,
                 _cc: str = None,
                 _bcc: str = None):

        self.EmailMessage = EmailMessage()
        self.EmailMessage['To'] = _email
        if _bcc is not None:
            self.EmailMessage['BCC'] = _bcc
        if _cc is not None:
            self.EmailMessage['CC'] = _cc
        if _subject is not None:
            self.EmailMessage['Subject'] = _subject
        self.attachments = _attachments
        self.html = _body
        self.marker = make_msgid()
        if _text is not None:
            self.text = _text
        else:
            self.text = self.convertBodyToText(_body)


    def send(self):
        self.addBody()
        for fileName in self.attachments:
            self.addFileToMail(fileName)
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.send_message(self.EmailMessage)
        except Exception as e:
            raise Exception("Error sending mail %s" % (str(e)))
        return self


    def setSender(self, _user, _email):
        self.EmailMessage['From'] = Address(_user, addr_spec=_email)
        return self


    @staticmethod
    def convertBodyToText(HTMLtext: str):
        soup = BeautifulSoup(HTMLtext, features="html.parser")
        return soup.get_text('\n')


    def addFileToMail(self, _filename: str):
        with open(_filename, "rb") as file:
            self.EmailMessage.add_attachment(file.read(),
                                             maintype="application",
                                             subtype="cnd.ms-excel",
                                             filename=basename(_filename))
        return self


    def addBody(self):
        self.EmailMessage.set_content(self.text)
        if self.html is not None:
            self.EmailMessage.add_alternative(self.html, subtype='html')
        return self
