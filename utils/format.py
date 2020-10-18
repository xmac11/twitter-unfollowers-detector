from datetime import datetime


def format_api_followers(api_followers):
    return {str(follower.id): follower.screen_name for follower in api_followers}


def format_file_data(current_followers):
    return {
        'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'count': len(current_followers),
        'followers': current_followers
    }


def format_unfollowers(*, old_followers, unfollower_ids):
    return {unfollower_id: old_followers[unfollower_id] for unfollower_id in unfollower_ids} if unfollower_ids else ""


def format_link_by_user_id(user_id):
    return f'https://twitter.com/i/user/{user_id}'
