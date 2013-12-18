
import sys
import os
import re
from smtplib import SMTP_SSL as SMTP
import email.MIMEText
import email.utils

class MySMTP (SMTP):

    def __init__(self, host, port, username=None, password=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def _login(self):
        self.server = SMTP(self.host, self.port)
        self.server.ehlo()
        #self.server.starttls()  
        #self.server.ehlo()
        self.server.login(self.username, self.password)  

    def sendemail(self, sender, destination, subject, content, text_subtype = 'plain'):
        """ typical values for text_subtype are plain, html, xml
        """
        msg = email.MIMEText.MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers will do this automatically, not all
        msg['To'] = destination
        #msg['X-Mailer'] = 'send-it-later'
        self.sendmime(sender, destination, msg)

    def sendmime(self, msg):
        self._login()
        self.server.set_debuglevel(False)
        try:
            self.server.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            self.server.close()

    def refresh(self, msg, subject):
        del msg['Subject']
        msg['Subject'] = subject
        del msg['Date']
        msg['Date'] = email.utils.formatdate()

    def logout(self):
        pass #self.server.quit()

