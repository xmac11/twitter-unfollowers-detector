import logging
import time
import traceback

import tweepy

from constants.emails import RATE_LIMIT_ERROR, GENERIC_ERROR
from constants.secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from utils.emails import send_email, send_email_with_results
from utils.files import write_json_file, read_json_file
from utils.format import format_api_followers, format_file_data, format_unfollowers
from utils.logging import setup_logger

logger = setup_logger(name='twitter-unfollowers', level=logging.INFO, filename='unfollowers.log')


def main():
    try:
        old_followers = read_old_followers()

        api = connect_to_api()
        api_followers = handle_rate_limit(tweepy.Cursor(api.followers).items())

        current_followers = format_api_followers(api_followers)
        save(current_followers)

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        logger.info(
            f'{len(unfollower_ids)} user(s) unfollowed you {format_unfollowers(old_followers=old_followers, unfollower_ids=unfollower_ids)}'
        )

        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        success_user_ids, error_user_ids = unfollow(api, ids_to_unfollow)

        send_email_with_results(
            success_user_ids=success_user_ids,
            error_user_ids=error_user_ids,
            no_need_to_unfollow_ids=no_need_to_unfollow_ids
        )
    except Exception as e:
        logger.exception(e)
        send_email(subject=GENERIC_ERROR, content=traceback.format_exc())


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


def save(current_followers):
    data = format_file_data(current_followers)
    write_json_file(data)


def find_unfollowers(*, old_followers, current_followers):
    return {user_id for user_id in set(old_followers).difference(set(current_followers))}


def find_ids_to_unfollow(*, old_followers, unfollower_ids):
    return {user_id for user_id in unfollower_ids if old_followers[user_id]['following']}


def find_no_need_to_unfollow_ids(*, unfollower_ids, ids_to_unfollow):
    return unfollower_ids.difference(ids_to_unfollow)


def unfollow(api, user_ids):
    success_user_ids = []
    error_user_ids = []

    for user_id in user_ids:
        try:
            user = api.destroy_friendship(user_id=user_id)
            success_user_ids.append(user.id)
            logger.info(f"Unfollowed {user.screen_name} (user_id='{user.id}')")
        except Exception as e:
            logger.exception(e)
            error_user_ids.append(user_id)

    return success_user_ids, error_user_ids


if __name__ == '__main__':
    main()
