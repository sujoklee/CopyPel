import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class CustomEmailSender(object):
    def __init__(self, sender, template_file=None):
        self.sender = sender
        self.template_path = template_file
        self.html = None
        if template_file:
            self._load_template()

    def _load_template(self):
        with open(self.template_path) as f:
            data = f.read()
        self.html = data

    def send_message(self, receivers, title, sender=None, **parameters):
        sender = self.sender or sender
        msg = MIMEMultipart()
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        result = self.html % parameters if parameters else self.html
        part1 = MIMEText(result, 'html')
        msg.attach(part1)
        s = smtplib.SMTP('localhost')
        s.set_debuglevel(True)
        try:
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        finally:
            s.quit()


if __name__ == '__main__':
    from forecast.settings import EMAIL_TEMPLATE_PATH
    c = CustomEmailSender('no-reply@peleus.com', EMAIL_TEMPLATE_PATH)
    c.send_message(['albert@collabimo.com'], 'new message')