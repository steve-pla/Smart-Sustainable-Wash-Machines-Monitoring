import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(recipient_email, name, subject, message, email_s, email_s_pass):
    flag = 0
    sender_email = email_s
    sender_password = email_s_pass
    # Create a MIME multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = 's.plastras@gmail.com'
    msg['Subject'] = subject + " \n \n --- [From email : " + \
                     recipient_email + ']' + "\n\n\n --- [From Name : " + name + ']'
    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    # Establish a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()

    try:
        # Login to the SMTP server
        server.login(sender_email, sender_password)
        # Send the email
        server.sendmail(sender_email, ['s.plastras@gmail.com', 'nrekkas@gmail.com'],
                        msg.as_string())
        flag = 1
    except smtplib.SMTPException as e:
        flag = -1
    finally:
        # Close the SMTP connection
        server.quit()
    return flag


