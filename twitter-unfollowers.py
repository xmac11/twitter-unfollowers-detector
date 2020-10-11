import logging
import os
import time
import traceback
from datetime import datetime

import tweepy

from constants.logs import FORMAT, DATE_FORMAT
from settings import LOGS_ROOT
from utils.emails import send_email
from utils.files import write_json_file, read_json_file

logger = logging.getLogger('twitter-unfollowers')
logging.basicConfig(filename=os.path.join(LOGS_ROOT, 'unfollowers.log'),
                    level=logging.INFO,
                    format=FORMAT,
                    datefmt=DATE_FORMAT)


# http://docs.tweepy.org/en/latest/code_snippet.html?highlight=cursor#handling-the-rate-limit-using-cursors
def handle_rate_limit(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            logger.error('RateLimitError, sleeping for 15 minutes...')
            send_email('RateLimitError occurred, sleeping for 15 minutes...')
            time.sleep(15 * 60)
        except StopIteration:
            break
        except Exception as e:
            logger.exception(e)
            send_email(traceback.format_exc())
            break


def main():
    consumer_key = os.environ['TWITTER-API-KEY']
    consumer_secret = os.environ['TWITTER-API-KEY-SECRET']
    access_token = os.environ['TWITTER-ACCESS-TOKEN']
    access_token_secret = os.environ['TWITTER-ACCESS-TOKEN-SECRET']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # old followers
    old_data = read_json_file()
    old_followers = old_data.get('followers', {})

    # current followers
    current_followers = {}
    for follower in handle_rate_limit(tweepy.Cursor(api.followers).items()):
        current_followers[str(follower.id)] = follower.screen_name

    data = {
        'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'count': len(current_followers),
        'followers': current_followers
    }
    write_json_file(data)

    # unfollowers
    unfollowers = {user_id: old_followers[user_id] for user_id in set(old_followers).difference(set(current_followers))}

    print(f'{len(unfollowers)} user(s) unfollowed you {unfollowers if len(unfollowers) > 0 else ""}')
    logger.info(f'{len(unfollowers)} user(s) unfollowed you {unfollowers if len(unfollowers) > 0 else ""}')

    # unfollow any unfollowers
    for user_id in unfollowers:
        user = api.destroy_friendship(user_id=user_id)
        print(f'Unfollowed {user}')
        logger.info(f"Unfollowed {user.screen_name} (user_id='{user.id}')")


if __name__ == '__main__':
    main()
