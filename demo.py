from imaptools import MyIMAP
import config

M = MyIMAP(config.imap_host, config.imap_port)
M.login(config.imap_username, config.imap_password)
M.select()

def testFolder(name):
    print "Nr in " + name, M.countMails(name, '(ALL)')
    print "Nr of SEEN in " + name, M.countMails(name, '(SEEN)')
    print "Nr of UNSEEN in " + name, M.countMails(name, '(UNSEEN)')
    print "Nr of NEW in " + name, M.countMails(name, '(NEW)')
    print "Nr of OLD in " + name, M.countMails(name, '(OLD)')
    print "Nr of RECENT in " + name, M.countMails(name, '(RECENT)')

testFolder('INBOX')
print "Nr of unread in Important", M.countMails('[Gmail]/Important', '(UNSEEN)')
print "Nr in Drafts", M.countMails('[Gmail]/Drafts', '(OLD)')
print
print "\n".join(M.listTasks('INBOX', '(ALL)'))

M.logout()

