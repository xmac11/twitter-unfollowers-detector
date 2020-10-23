from datetime import datetime


def format_api_followers(api_followers):
    return {
        str(follower.id): {
            'screen_name': follower.screen_name,
            'following': follower.following
        } for follower in api_followers
    }


def format_file_data(current_followers):
    return {
        'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'count': len(current_followers),
        'followers': current_followers
    }


def format_unfollowers(*, old_followers, unfollower_ids):
    return {unfollower_id: old_followers[unfollower_id]['screen_name'] for unfollower_id in unfollower_ids} if unfollower_ids else ""


def format_message(*, message, user_ids):
    return f'{message}\n{format_user_ids_as_links(user_ids)}' if user_ids else ''


def format_user_ids_as_links(user_ids):
    return '\n'.join([f'https://twitter.com/i/user/{user_id}' for user_id in user_ids])
