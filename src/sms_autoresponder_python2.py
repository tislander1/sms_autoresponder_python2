import smtplib
import imaplib
import email
import re
import thread
import threading
import time

SENDER = 'XXX@gmail.com'
RECIPIENT = 'YYY@gmail.com'
PASSWORD = 'ZZZ'
PHONE = '5551234567@mms.att.net'

class Operation(threading._Timer):
    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        while True:
            self.finished.clear()
            self.finished.wait(self.interval)
            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
            else:
                return
            self.finished.set()

class Manager(object):
    ops = []
    def add_operation(self, operation, interval, args=[], kwargs={}):
        op = Operation(interval, operation, args, kwargs)
        self.ops.append(op)
        thread.start_new_thread(op.run, ())
    def stop(self):
        for op in self.ops:
            op.cancel()
        self._event.set()
        
def send_gmail(body, subject, recipient=RECIPIENT):
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
     
    sender = SENDER
    password = PASSWORD
     
    "Sends an e-mail to the specified recipient."
     
    body = "" + body + ""
     
    headers = ["From: " + sender,
               "Subject: " + subject,
               "To: " + recipient,
               "MIME-Version: 1.0",
               "Content-Type: text/plain"]
    headers = "\r\n".join(headers)
     
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
     
    session.ehlo()
    session.starttls()
    session.ehlo
    session.login(sender, password)
     
    session.sendmail(sender, recipient, headers + "\r\n\r\n" + body)
    session.quit()

    print 'Email sent.'

def convertDate(date):
    import time
    #import datetime
    from dateutil import parser

    date = parser.parse(date)
    date = date.timetuple()
    date = time.mktime(date)
    return date

def get_gmail(email_subject, email_sender = SENDER):
    IMAP_SERVER='imap.gmail.com'
    IMAP_PORT=993
     
    M = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    rc, resp = M.login(SENDER, PASSWORD)
    print rc, resp
    print ""

    M.select()
    #typ, data = M.search(None, 'ALL')
    search_string = '(FROM "'+ email_sender + '" SUBJECT "' + email_subject +'")'
    typ, data = M.search(None, search_string)

    email_list =[]
    
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        date = M.fetch(num, '(INTERNALDATE)')[1][0].split("\"")[1]
        email_part_0 = (date, convertDate(date))
        #print 'Message %s\n%s\n' % (num, data[0][1])

        mail = email.message_from_string(data[0][1])

        msg = email.parser.HeaderParser().parsestr(data[0][1])
        email_part_1 = msg['From']
        email_part_2 = msg['To']
        email_part_3 = msg['Subject']
        
        for part in mail.walk():
            # multipart are just containers, so we skip them
            if part.get_content_maintype() == 'multipart':
                continue
            email_part_4 = part.get_payload()
            #print "here is email part 3: " + email_part_3
            table_data = re.search(r"()(.*)()", email_part_4, re.DOTALL)
            if table_data:
                email_part_4 = table_data.group(2).strip()
                #print "Removed email formatting."
            

        email_list.append((email_part_0, email_part_1, email_part_2, email_part_3, email_part_4))
        
    M.close()
    M.logout()
    return email_list

def get_new_gmail(last_time, email_subject, email_sender = SENDER):
    all_email_list = get_gmail(email_subject, email_sender)
    new_email_list = []
    max_time = last_time
    for email in all_email_list:
        if email[0][1] > last_time:
            new_email_list.append(email)
        if email[0][1] > max_time:
            max_time = email[0][1]
    return (new_email_list, max_time)


##emails = get_gmail("", PHONE)


def turn_on_light():
    msg = "OK, turned on the light"
    print msg
    send_gmail(msg, "Python", PHONE)

def turn_off_light():
    msg = "OK, turned off the light"
    print msg
    send_gmail(msg, "Python", PHONE)
    

def check_email():
    global max_time
    (new_emails, max_time) = get_new_gmail(max_time, "", PHONE)
    #print new_emails
    for email in new_emails:
        email_text = email[4]
        if re.search(r"off.*light", email_text):
            turn_off_light()
            continue
        if re.search(r"on.*light", email_text):
            turn_on_light()
            continue
            
print "Starting program"
max_time = 0
timer = Manager()
timer.add_operation(check_email, 5*60)   #Check email every 5 minutes
while True:
    time.sleep(.1)
