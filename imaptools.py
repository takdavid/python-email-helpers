
import imaplib
import email.parser, email.header
import quopri
from email.MIMEText import MIMEText

class MyIMAP (imaplib.IMAP4_SSL):

    def countMails(self, mailbox="INBOX", criterion="(ALL)"):
        res = -1
        typ, msgnums = self.select(mailbox, True)
        try:
            if criterion != "(ALL)":
                typ, msgnums = self.search('UTF-8', criterion)
            cnt = len(msgnums[0].split())
            if typ == "OK":
                res = cnt
                self.close()
        except imaplib.IMAP4.error as e:
            print "ERROR", str(e)
        except Exception as e:
            raise e
            #return -1
        return res

    def listTasks(self, mailbox="INBOX", criterion="(ALL)"):
        res = []
        self.select(mailbox, True)
        typ, msgnums = self.search('UTF-8', criterion)
        for num in msgnums[0].split():
            typ, data = self.fetch(num, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
            parser = email.parser.HeaderParser()
            msg = parser.parsestr(data[0][1])
            text = headerUnicode(msg['From']) + " : " + headerUnicode(msg['Subject'])
            res.append(text)
        return res

    def nums(self, mailbox="INBOX", criterion="(ALL)"):
        self.select(mailbox, True)
        typ, msgnums = self.search('UTF-8', criterion)
        return msgnums[0].split()

    def asMIMEText(self, num):
        typ, data = self.fetch(num, '(RFC822)')
        parser = email.parser.Parser()
        msg = parser.parsestr(data[0][1])
        return msg

    def delete(self, num, fromfolder='[Gmail]/Drafts', tofolder='[Gmail]/Trash'):
        if fromfolder:
            self.select(fromfolder)
            self.uid('STORE', num, '-X-GM-LABELS', fromfolder)
        if tofolder:
            self.uid('COPY', num, tofolder)
            self.uid('STORE', num, '+X-GM-LABELS', tofolder)
        self.uid('STORE', num, '+FLAGS', '(\Deleted)')
        self.store(num, '+FLAGS', '\\Deleted')
        self.expunge()

def headerUnicode(mimebytestring):
    h = email.header.decode_header(mimebytestring)
    res = []
    for hh in h:
        if hh[1] is None:
            res.append(unicode(quopri.decodestring(hh[0])))
        else:
            res.append(unicode(quopri.decodestring(hh[0]).decode(hh[1])))
    return u" ".join(res)

