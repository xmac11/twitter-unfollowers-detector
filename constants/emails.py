import os

FROM_ADDRESS = ''  # 'from' address goes here (Note that SMTP_HOST is configured as gmail)
TO_ADDRESS = ''  # 'to' address goes here

EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

RATE_LIMIT_ERROR = 'RateLimitError in twitter-unfollowers script'
ERROR_UNFOLLOWING = 'Exception while unfollowing user(s) in twitter-unfollowers script'
GENERIC_ERROR = 'Problem with twitter-unfollowers script'
