import smtplib 
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 
from application.config import *

from weasyprint import HTML
from jinja2 import Template


def create_pdf_report(html_string, pdf_path): #function for converting the html to pdf
    html = HTML(string = html_string)
    html.write_pdf(target = pdf_path)
    

def send_email(to_address,subject,message,user,content="text"): #function for sending the email to the user
    msg = MIMEMultipart()
    msg['To']=to_address
    msg['From']=SENDER_ADDRESS
    msg['Subject']=subject
    if content == "html": #checking whether the content passed is html or text
        msg.attach(MIMEText(message,'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))

    pdf_file_path = f"./static/{ user }_report.pdf"
    create_pdf_report(message,pdf_file_path)


    with open(pdf_file_path,"rb") as a:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(a.read())
    encoders.encode_base64(part)
    # part.add_header("Content-Disposition", f"attachment;filename={pdf_file_path}")
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % pdf_file_path)
    msg.attach(part)          

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT )
    s.login(SENDER_ADDRESS,SENDER_PASSWORD) #logging into mail hog with the admin credentials
    s.send_message(msg) #sending the emails
    s.quit()
    return True
