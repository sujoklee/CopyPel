import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class CustomEmailSender(object):
    def __init__(self, server, username, password, template_file=None):
        self.server = server
        self.username = username
        self.password = password
        self.template_path = template_file
        self.html = None
        if template_file:
            self._load_template()

    def _load_template(self):
        with open(self.template_path) as f:
            data = f.read()
        self.html = data

    def send_message(self, receivers, title, **parameters):
        msg = MIMEMultipart()
        msg['Subject'] = title
        msg['From'] = self.username
        msg['To'] = ','.join(receivers)
        result = self.html % parameters if parameters else self.html
        part1 = MIMEText(result, 'html')
        msg.attach(part1)
        s = smtplib.SMTP(self.server)
        s.starttls()
        s.login(self.username, self.password)
        try:
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            s.quit()


if __name__ == '__main__':
    pass