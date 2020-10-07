#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 10:03:16 2020

@author: alberttenigin
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
user = 'teniginalbert@gmail.com'

password = read_password()
 
recipients = ['vyalshin.emil@yandex.ru', 'vyalshin.emil@gmail.com']
sender = 'teniginalbert@gmail.com'
subject = 'Bewerbung von Emil Wjalschin 1'

text_str = 'Guten Morgen!\n\nMein Name ist Emil Wjalschin, \
    ich bin ein Elektronikingenieur aus Russland. Ich habe Ihre Firma bei wlw gefunden und\
        ich bin sehr interessiert an der Möglichkeit, für Ihr Unternehmen zu arbeiten. \
            Haben Sie freie Stellen für die Position eines Elektronikingenieurs oder eine gleichwertige Stelle?\n\n\
                Mein CV und Diplom im Anhang\n\
                    —\n\
                        Mit freundlichen Grüßen,\n\
                            Emil Wjalschin\n\
                                Russland, Sankt Petersburg\n\
                                    Telefon: +7 (999) 512-69-75\n\
                                        Viber: +7 (999) 512-69-75\n\
                                            WhatsApp: +7 (999)512-69-75'
texts = ['Guten Morgen!',\
         '',
         'Mein Name ist Emil Wjalschin, ich bin ein Elektronikingenieur aus Russland. \
             Ich habe Ihre Firma bei wlw gefunden und ich bin sehr interessiert an der Möglichkeit, \
                 für Ihr Unternehmen zu arbeiten. Haben Sie freie Stellen für die Position eines Elektronikingenieurs \
            oder eine gleichwertige Stelle?',\
         '',\
        'Mein CV und Diplom im Anhang',\
        '—',\
        'Mit freundlichen Grüßen',\
        'Emil Wjalschin',\
        'Russland, Sankt Petersburg',\
        'Telefon: +7 (999) 512-69-75',\
        'Viber: +7 (999) 512-69-75',\
        'WhatsApp: +7 (999)512-69-75']
                            
text = '<br>'.join(texts)

html = '<html><head></head><body><p>'+text+'</p></body></html>'
  
part_text = MIMEText(text_str, 'plain')
part_html = MIMEText(html, 'html') 

filepath_1 = "/home/alberttenigin/projects/mail_sender/CV.docx"
basename_1 = os.path.basename(filepath_1)
filesize_1 = os.path.getsize(filepath_1)
filepath_2 = "/home/alberttenigin/projects/mail_sender/diploma.jpg"
basename_2 = os.path.basename(filepath_2)
filesize_2 = os.path.getsize(filepath_2)

part_file_1 = MIMEBase('application', 'octet-stream; name="{}"'.format(basename_1))
part_file_1.set_payload(open(filepath_1,"rb").read() )
part_file_1.add_header('Content-Description', basename_1)
part_file_1.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename_1, filesize_1))
encoders.encode_base64(part_file_1)

part_file_2 = MIMEBase('application', 'octet-stream; name="{}"'.format(basename_2))
part_file_2.set_payload(open(filepath_2,"rb").read() )
part_file_2.add_header('Content-Description', basename_2)
part_file_2.add_header('Content-Disposition', 'attachment; filename="{}"; size={}'.format(basename_2, filesize_2))
encoders.encode_base64(part_file_2)
 
mail = smtplib.SMTP_SSL(server)
mail.login(user, password)
#mail.sendmail(sender, recipients, msg.as_string())

for recipient in recipients:
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Albert Tenigin <' + sender + '>'
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/'+(python_version())

    msg.attach(part_text)
    msg.attach(part_html)
    msg['To'] = recipient
    msg.attach(part_file_1)
    msg.attach(part_file_2)
    #mail.sendmail(sender, recipient, msg.as_string())
    mail.send_message(msg)

mail.quit()