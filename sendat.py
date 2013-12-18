import smtptools
import imaptools
from config import *
from dateutil import parser
import re
import datetime

def parseAt(msg):
    m = re.search('^\[at\s*(.*?)\]\s*(.*)$', imaptools.headerUnicode(msg['Subject']))
    if m:
        return parser.parse(m.group(1)), m.group(2)
    return None, msg['Subject']

S = smtptools.MySMTP(smtp_host, smtp_port, smtp_username, smtp_password)
M = imaptools.MyIMAP(imap_host, imap_port)
M.login(imap_username, imap_password)
nums = M.nums("[Gmail]/Drafts")
deletable = []
for num in nums:
    msg = M.asMIMEText(num)
    at, subject = parseAt(msg)
    if at:
        print "SEND "+subject.encode('UTF-8')+" AT "+str(at),
        if at < datetime.datetime.now():
            print "NOW"
            S.refresh(msg, subject)
            S.sendmime(msg)
            deletable.append(num)
        else:
            print "LATER"
    else:
        print "SKIP "+imaptools.headerUnicode(subject).encode('UTF-8')
map(M.delete, deletable)
M.logout()
S.logout()
