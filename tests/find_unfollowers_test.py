import unittest

from twitter_unfollowers import find_unfollowers


class FindUnfollowersTest(unittest.TestCase):

    def test_find_unfollowers_with_no_followers(self):
        old_followers = {}
        current_followers = {}

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, set())

    def test_find_unfollowers_with_same_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, set())

    def test_find_unfollowers_with_new_follower_and_no_unfollowers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, set())

    def test_find_unfollowers_with_one_unfollower_and_no_new_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, {'00003'})

    def test_find_unfollowers_with_multiple_unfollowers_and_no_new_follower(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True},
            '00004': {'screen_name': 'follower4', 'following': True},
            '00005': {'screen_name': 'follower5', 'following': True}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, {'00002', '00004', '00005'})

    def test_find_unfollowers_with_multiple_unfollowers_and_new_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True},
            '00004': {'screen_name': 'follower4', 'following': True},
            '00005': {'screen_name': 'follower5', 'following': True}
        }
        current_followers = {
            '00002': {'screen_name': 'follower2', 'following': True},
            '00004': {'screen_name': 'follower4', 'following': True},
            '00006': {'screen_name': 'follower6', 'following': True},
            '00007': {'screen_name': 'follower7', 'following': True}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, {'00001', '00003', '00005'})

    def test_find_unfollowers_when_all_unfollow(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True}
        }
        current_followers = {}

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollower_ids, old_followers.keys())


if __name__ == '__main__':
    unittest.main()
