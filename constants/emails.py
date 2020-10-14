import os

FROM_ADDRESS = ''  # 'from' address goes here (Note that SMTP_HOST is configured as gmail)
TO_ADDRESS = ''  # 'to' address goes here

EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465
