import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import email


from jinja2 import Template
SMPTP_SERVER_HOST = 'localhost'

SMPTP_SERVER_PORT = 1025        #default port from smtp server MAILHOG (install MAILHOG)
SENDER_ADDRESS="email@kailash.com"
SENDER_PASSWORD =""

def send_email(to_address,subject,message ,
               content="text", attachment_file=None ):
    msg=MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to_address
    msg['Subject'] = subject
    
    if content == 'html':
        msg.attach(MIMEText(message, 'html'))
    else:
        msg.attach(MIMEText(message, 'plain'))
    
    if attachment_file:
        with open(attachment_file, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        # part.add_header('Content-Disposition', 'attachment', filename=attachment_file)
            # msg.attach(part)
        msg.attach(part)
    
        

    s=smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.quit()
    return True
def format_message(template_file, data={}):
    with open(template_file) as file:
        template = Template(file.read())
        return template.render(data=data)
    
    
    
def send_welcome_message(data):
    message = format_message('welcome-email.html', data=data)
    send_email(
        to_address=data['email'],
        subject='Welcome',
        message=message,
        content='html',
        # attachment_file=manual.pdf
    )

def main():
    
    new_users=[
        {
                "name":"Kailash",
                "email":"email@kailash.com"
            },
            {
                "name":"kamal",
                "email":"email@kamal.com"
            },
            
    ]
        
    for user in new_users:
        send_welcome_message(user)
        
if __name__ == '__main__':
    main()
