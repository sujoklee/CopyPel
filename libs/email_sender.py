import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class CustomEmailSender(object):
    def __init__(self, sender, template_file=None):
        self.sender = sender
        self.template_path = template_file
        self.html = None

    def load_template(self):
        with open(self.template_path) as f:
            data = f.read()
        self.html = data

    def send_message(self, receivers, title, sender=None, **parameters):
        sender = self.sender or sender
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = receivers

        part1 = MIMEText(self.html % parameters, 'html')
        msg.attach(part1)
        s = smtplib.SMTP('localhost')
        s.sendmail(sender, receivers, msg.as_string())
        s.quit()


if __name__ == '__main__':
    c = CustomEmailSender()