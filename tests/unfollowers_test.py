import unittest

from twitter_unfollowers import find_unfollowers, find_ids_to_unfollow, find_no_need_to_unfollow_ids


class UnfollowersTest(unittest.TestCase):

    def test_with_no_followers(self):
        old_followers = {}
        current_followers = {}

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, set())
        self.assertEqual(ids_to_unfollow, set())
        self.assertEqual(no_need_to_unfollow_ids, set())

    def test_with_same_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, set())
        self.assertEqual(ids_to_unfollow, set())
        self.assertEqual(no_need_to_unfollow_ids, set())

    def test_with_new_follower_and_no_unfollowers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False},
            '00003': {'screen_name': 'follower3', 'following': False}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, set())
        self.assertEqual(ids_to_unfollow, set())
        self.assertEqual(no_need_to_unfollow_ids, set())

    def test_with_one_unfollower_whom_i_was_following_and_no_new_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False},
            '00003': {'screen_name': 'follower3', 'following': True}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, {'00003'})
        self.assertEqual(ids_to_unfollow, {'00003'})
        self.assertEqual(no_need_to_unfollow_ids, set())

    def test_with_one_unfollower_whom_i_was_not_following_and_no_new_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False},
            '00003': {'screen_name': 'follower3', 'following': False}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, {'00003'})
        self.assertEqual(ids_to_unfollow, set())
        self.assertEqual(no_need_to_unfollow_ids, {'00003'})

    def test_with_multiple_unfollowers_and_no_new_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True},
            '00004': {'screen_name': 'follower4', 'following': False},
            '00005': {'screen_name': 'follower5', 'following': True}
        }
        current_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, {'00002', '00004', '00005'})
        self.assertEqual(ids_to_unfollow, {'00002', '00005'})
        self.assertEqual(no_need_to_unfollow_ids, {'00004'})

    def test_with_multiple_unfollowers_whom_i_was_not_following_and_new_followers(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False},
            '00003': {'screen_name': 'follower3', 'following': False},
            '00004': {'screen_name': 'follower4', 'following': False},
            '00005': {'screen_name': 'follower5', 'following': False}
        }
        current_followers = {
            '00002': {'screen_name': 'follower2', 'following': False},
            '00004': {'screen_name': 'follower4', 'following': False},
            '00006': {'screen_name': 'follower6', 'following': False},
            '00007': {'screen_name': 'follower7', 'following': False}
        }

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, {'00001', '00003', '00005'})
        self.assertEqual(ids_to_unfollow, set())
        self.assertEqual(unfollower_ids, {'00001', '00003', '00005'})

    def test_when_all_unfollow_and_i_was_following_them(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': True},
            '00002': {'screen_name': 'follower2', 'following': True},
            '00003': {'screen_name': 'follower3', 'following': True}
        }
        current_followers = {}

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, {'00001', '00002', '00003'})
        self.assertEqual(ids_to_unfollow, {'00001', '00002', '00003'})
        self.assertEqual(no_need_to_unfollow_ids, set())

    def test_when_all_unfollow_and_i_was_not_following_them(self):
        old_followers = {
            '00001': {'screen_name': 'follower1', 'following': False},
            '00002': {'screen_name': 'follower2', 'following': False},
            '00003': {'screen_name': 'follower3', 'following': False}
        }
        current_followers = {}

        unfollower_ids = find_unfollowers(old_followers=old_followers, current_followers=current_followers)
        ids_to_unfollow = find_ids_to_unfollow(old_followers=old_followers, unfollower_ids=unfollower_ids)
        no_need_to_unfollow_ids = find_no_need_to_unfollow_ids(unfollower_ids=unfollower_ids, ids_to_unfollow=ids_to_unfollow)

        self.assertEqual(unfollower_ids, {'00001', '00002', '00003'})
        self.assertEqual(ids_to_unfollow, set())
        self.assertEqual(no_need_to_unfollow_ids, {'00001', '00002', '00003'})


if __name__ == '__main__':
    unittest.main()
