import datetime
import hashlib
import jwt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class HashFile(object):
    def __init__(self, filename, blocksize = 65536):
        file_hash = hashlib.sha256()
        with open(filename, 'rb') as f:
            fb = f.read(blocksize)
            while len(fb) > 0:
                file_hash.update(fb)
                fb = f.read(blocksize)

        self.digest = file_hash.hexdigest()

    def getDigest(self):
        return self.digest


class TokenManager(object):
    def __init__(self, appkey, algorithm="HS256"):
        self.key = appkey
        self.algo = algorithm

    def gen_token(self, ibmserial, week):
        token = jwt.encode(
            {
                'ibmserial': ibmserial,
                'week': week,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=48)
            },
            self.key, algorithm=self.algo)

        return token

    def verify_token(self, token):
        try:
            data = jwt.decode(token, self.key, algorithms=[self.algo])
            if not data['ibmserial'] or not data['week']:
                data = {'error': 'Invalid token, required fields missing'}
        except Exception as e:
            data = {'error': f'{str(e)}'}

        return data


class Mailer(object):
    def __init__(self, password, sender):
        self.sender = sender
        self.password = password

    def send(self, receiver, mail_message):
        message = MIMEMultipart("alternative")
        message["Subject"] = "ILC CTE variance"
        message["From"] = self.sender
        message["To"] = receiver
        part = MIMEText(mail_message, "html")
        message.attach(part)
        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, receiver, message.as_string())
                server.quit()
            return True, 'Success'
        except Exception as e:
            return False, e
