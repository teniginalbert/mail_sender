#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:03:16 2020

@author: alberttenigin
"""

"""

    Critical lines for changing:
        50 : server of your mail provider
        51 : username for mail
        55 : recipients
        56 : sender name
        57 : subject of the letter
        59 : raw formatted text
        62 : list of lines to be html-formatted
        71 : files sources
   109-114 : msg parameters 
   
   ALSO! you must create config.txt with your password
    
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version

def read_password():    
   dir = os.path.dirname(os.path.abspath(__file__))
   try:
       f = open(dir + '/config.txt','r')
   except FileNotFoundError:
       print('cannot find password file!')
       return ''
   try:
       contents = f.readlines()
   except SyntaxError:
       print('password file reading error!')
       return ''
   else:
       print('reading password is ok')
   f.close()

   return contents[0]

server = 'smtp.gmail.com'
user = 'yourmail@gmail.com'

password = read_password()
 
recipients = ['recipient1@gmail.com', 'recipient2@gmail.com']
sender = 'yourmail@gmail.com'
subject = 'yoursubject'

text_str = 'Hello \
            My name is X \
                Goodbye'
texts = ['Hello', '', 'My name is X', '','Goodbye']
                            
text = '<br>'.join(texts)

html = '<html><head></head><body><p>'+text+'</p></body></html>'
  
part_text = MIMEText(text_str, 'plain')
part_html = MIMEText(html, 'html') 

filepaths = ["abs_path_to_your_file", "abs_path_to_another"]
basenames = list(map(os.path.basename(), filepaths))
filesizes = list(map(os.path.getsize(), filepaths))
#filepath_1 = "/home/alberttenigin/projects/mail_sender/CV.docx"
#basename_1 = os.path.basename(filepath_1)
#filesize_1 = os.path.getsize(filepath_1)
#filepath_2 = "/home/alberttenigin/projects/mail_sender/diploma.jpg"
#basename_2 = os.path.basename(filepath_2)
#filesize_2 = os.path.getsize(filepath_2)


part_files = []

for bn, fp, fs in zip(basenames, filepaths, filesizes):
    part_file = MIMEBase('application', 'octet-stream; name="{}"'.format(bn))
    part_file.set_payload(open(fp,"rb").read() )
    part_file.add_header('Content-Description', bn)
    part_file.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(bn, fs))
    encoders.encode_base64(part_file)
    part_files.append(part_file)
"""
part_file_1 = MIMEBase('application', 'octet-stream; name="{}"'.format(basenames[1]))
part_file_1.set_payload(open(filepaths[0],"rb").read() )
part_file_1.add_header('Content-Description', basename_1)
part_file_1.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename_1, filesize_1))
encoders.encode_base64(part_file_1)

part_file_2 = MIMEBase('application', 'octet-stream; name="{}"'.format(basename_2))
part_file_2.set_payload(open(filepath_2,"rb").read() )
part_file_2.add_header('Content-Description', basename_2)
part_file_2.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename_2, filesize_2))
encoders.encode_base64(part_file_2)
"""
mail = smtplib.SMTP_SSL(server)
mail.login(user, password)
#mail.sendmail(sender, recipients, msg.as_string())

for recipient in recipients:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'My Name <' + sender + '>'
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/'+(python_version())

    msg.attach(part_text)
    msg.attach(part_html)
    msg['To'] = recipient
    for pf in part_files:
        msg.attach(pf)
   # msg.attach(part_file_2)
    #mail.sendmail(sender, recipient, msg.as_string())
    mail.send_message(msg)

mail.quit()