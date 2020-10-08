from datetime import datetime
import json
import logging
import os
import time

import tweepy

logging.basicConfig(filename='unfollowers.log',
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')


def write_json_file(data):
    with open('followers.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_json_file():
    try:
        with open('followers.json') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# http://docs.tweepy.org/en/latest/code_snippet.html?highlight=cursor#handling-the-rate-limit-using-cursors
def handle_rate_limit(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            logging.error('RateLimitError, sleeping for 15 minutes...')
            time.sleep(15 * 60)
        except StopIteration:
            break
        except Exception as e:
            logging.exception(e)
            break


def main():
    consumer_key = os.environ.get('TWITTER-API-KEY')
    consumer_secret = os.environ.get('TWITTER-API-KEY-SECRET')
    access_token = os.environ.get('TWITTER-ACCESS-TOKEN')
    access_token_secret = os.environ.get('TWITTER-ACCESS-TOKEN-SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # old followers
    old_data = read_json_file()
    old_followers = old_data.get('followers', {})

    # current followers
    data = {}
    current_followers = {}
    for follower in handle_rate_limit(tweepy.Cursor(api.followers).items()):
        current_followers[str(follower.id)] = follower.screen_name

    data['date'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data['count'] = len(current_followers)
    data['followers'] = current_followers
    write_json_file(data)

    # unfollowers
    unfollowers = {user_id: old_followers[user_id] for user_id in set(old_followers).difference(set(current_followers))}

    print(f'{len(unfollowers)} user(s) unfollowed you {unfollowers if len(unfollowers) > 0 else ""}')
    logging.info(f'{len(unfollowers)} user(s) unfollowed you {unfollowers if len(unfollowers) > 0 else ""}')

    # unfollow any unfollowers
    for user_id in unfollowers:
        user = api.destroy_friendship(user_id=user_id)
        print(f'Unfollowed {user}')
        logging.info(f"Unfollowed {user.screen_name} (user_id='{user.id}')")


if __name__ == '__main__':
    main()
