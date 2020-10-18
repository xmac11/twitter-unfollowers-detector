import logging
import os
import time
import traceback

import tweepy

from constants.emails import RATE_LIMIT_ERROR, ERROR_UNFOLLOWING, GENERIC_ERROR
from constants.logs import FORMAT, DATE_FORMAT
from constants.twitter import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from settings import LOGS_ROOT
from utils.emails import send_email
from utils.files import write_json_file, read_json_file
from utils.format import format_api_followers, format_file_data, format_unfollowers, format_link_by_user_id

logger = logging.getLogger('twitter-unfollowers')
logging.basicConfig(filename=os.path.join(LOGS_ROOT, 'unfollowers.log'),
                    level=logging.INFO,
                    format=FORMAT,
                    datefmt=DATE_FORMAT)


def main():
    # old followers
    old_followers = read_old_followers()

    # connect to API
    api = connect_to_api()
    api_followers = handle_rate_limit(tweepy.Cursor(api.followers).items())

    # current followers
    current_followers = format_api_followers(api_followers)
    save(current_followers)

    # unfollowers
    unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

    print(f'{len(unfollower_ids)} user(s) unfollowed you {format_unfollowers(old_followers=old_followers, unfollower_ids=unfollower_ids)}')
    logger.info(f'{len(unfollower_ids)} user(s) unfollowed you {format_unfollowers(old_followers=old_followers, unfollower_ids=unfollower_ids)}')

    # unfollow any unfollowers
    unfollow(api, unfollower_ids)


def read_old_followers():
    old_data = read_json_file()
    return old_data.get('followers', {})


def connect_to_api():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)


# http://docs.tweepy.org/en/latest/code_snippet.html?highlight=cursor#handling-the-rate-limit-using-cursors
def handle_rate_limit(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            logger.error('RateLimitError, sleeping for 15 minutes...')
            send_email(subject=RATE_LIMIT_ERROR, content='RateLimitError, sleeping for 15 minutes...')
            time.sleep(15 * 60)
        except StopIteration:
            break
        except Exception as e:
            logger.exception(e)
            send_email(subject=GENERIC_ERROR, content=traceback.format_exc())
            break


def save(current_followers):
    data = format_file_data(current_followers)
    write_json_file(data)


def find_unfollowers(*, old_followers, current_followers):
    return {user_id for user_id in set(old_followers).difference(set(current_followers))}


def unfollow(api, user_ids):
    error_user_ids = []
    for user_id in user_ids:
        try:
            user = api.destroy_friendship(user_id=user_id)
            print(f'Unfollowed {user}')
            logger.info(f"Unfollowed {user.screen_name} (user_id='{user.id}')")
        except Exception as e:
            logger.exception(e)
            error_user_ids.append(user_id)

    if error_user_ids:
        content = '\n'.join([format_link_by_user_id(user_id) for user_id in error_user_ids])
        send_email(subject=ERROR_UNFOLLOWING, content=content)


if __name__ == '__main__':
    main()
