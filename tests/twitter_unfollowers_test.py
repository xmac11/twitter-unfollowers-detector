import unittest

from twitter_unfollowers import find_unfollowers


class UnfollowersTest(unittest.TestCase):

    def test_find_unfollowers_with_no_followers(self):
        old_followers = {}
        current_followers = {}

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, set())

    def test_find_unfollowers_with_same_followers(self):
        old_followers = {
            '00001': 'follower1',
            '00002': 'follower2'
        }
        current_followers = {
            '00001': 'follower1',
            '00002': 'follower2',
        }

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, set())

    def test_find_unfollowers_with_new_follower_and_no_unfollowers(self):
        old_followers = {
            '00001': 'follower1',
            '00002': 'follower2'
        }
        current_followers = {
            '00001': 'follower1',
            '00002': 'follower2',
            '00003': 'follower3'
        }

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, set())

    def test_find_unfollowers_with_one_unfollower_and_no_new_followers(self):
        old_followers = {
            '00001': 'follower1',
            '00002': 'follower2',
            '00003': 'follower3'
        }
        current_followers = {
            '00001': 'follower1',
            '00002': 'follower2'
        }

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, {'00003'})

    def test_find_unfollowers_with_multiple_unfollowers_and_no_new_follower(self):
        old_followers = {
            '00001': 'follower1',
            '00002': 'follower2',
            '00003': 'follower3',
            '00004': 'follower4',
            '00005': 'follower5'
        }
        current_followers = {
            '00001': 'follower1',
            '00003': 'follower3'
        }

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, {'00002', '00004', '00005'})

    def test_find_unfollowers_with_multiple_unfollowers_and_new_followers(self):
        old_followers = {
            '00001': 'follower1',
            '00002': 'follower2',
            '00003': 'follower3',
            '00004': 'follower4',
            '00005': 'follower5'
        }
        current_followers = {
            '00002': 'follower2',
            '00004': 'follower4',
            '00006': 'follower6',
            '00007': 'follower7'
        }

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, {'00001', '00003', '00005'})

    def test_find_unfollowers_when_all_unfollow(self):
        old_followers = {
            '00001': 'follower1',
            '00002': 'follower2'
        }
        current_followers = {}

        unfollowers = find_unfollowers(old_followers=old_followers, current_followers=current_followers)

        self.assertEqual(unfollowers, old_followers.keys())


if __name__ == '__main__':
    unittest.main()
