
import smtplib

GMAIL_USER = 'host emaila ddress' # replace "userID" with a valid gmail user ID
GMAIL_PASS = 'password'       # replace "mypassword" with the user's password
                                
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

def send_email(recipient, subject, text):
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + recipient + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + subject + '\n'
    msg = header + '\n' + text + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, recipient, msg)
    smtpserver.close()

if __name__ == '__main__':
    # replace "some email address" with a destination email address
    send_email('email adress', 'subject', 'message')

#Author of code: Ljubomir Perkovic
Downloaded from: http://reed.cs.depaul.edu/lperkovic/csc299/lab3/sendmail.py
