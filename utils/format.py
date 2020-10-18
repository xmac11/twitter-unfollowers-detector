def format_api_followers(api_followers):
    return {str(follower.id): follower.screen_name for follower in api_followers}


def format_unfollowers(*, old_followers, unfollower_ids):
    return {unfollower_id: old_followers[unfollower_id] for unfollower_id in unfollower_ids}
