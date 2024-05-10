from unittest import TestCase

from views import FixedFriendsUpdates, create_update


class TestSocial(TestCase):
    def test_create_update_with_valid_inputs(self):
        image_url = FixedFriendsUpdates.FRIEND_1.value[0]
        text = FixedFriendsUpdates.FRIEND_1.value[1]
        update = create_update(image_url, text)
        self.assertIsNotNone(update)

    def test_create_update_with_empty_image_url(self):
        image_url = ""
        text = FixedFriendsUpdates.FRIEND_1.value[1]
        with self.assertRaises(ValueError):
            create_update(image_url, text)

    def test_create_update_with_empty_text(self):
        image_url = FixedFriendsUpdates.FRIEND_1.value[0]
        text = ""
        with self.assertRaises(ValueError):
            create_update(image_url, text)

    def test_create_update_with_none_inputs(self):
        image_url = None
        text = None
        with self.assertRaises(ValueError):
            create_update(image_url, text)

    def test_create_update_with_invalid_image_url_type(self):
        image_url = 123
        text = FixedFriendsUpdates.FRIEND_1.value[1]
        with self.assertRaises(TypeError):
            create_update(image_url, text)

    def test_create_update_with_too_long_text(self):
        image_url = FixedFriendsUpdates.FRIEND_1.value[0]
        text = "a" * 40
        with self.assertRaises(ValueError):
            create_update(image_url, text)


class TestFixedFriendsUpdates(TestCase):
    def test_all_fixed_friends_updates_have_valid_urls(self):
        for friend_update in FixedFriendsUpdates:
            image_url = friend_update.value[0]
            self.assertIsInstance(image_url, str)
            self.assertTrue(image_url.startswith('http'))

    def test_all_fixed_friends_updates_have_non_empty_texts(self):
        for friend_update in FixedFriendsUpdates:
            text = friend_update.value[1]
            self.assertIsInstance(text, str)
            self.assertTrue(len(text) > 0)

    def test_all_fixed_friends_updates_have_text_lengths_less_than_35(self):
        for friend_update in FixedFriendsUpdates:
            text = friend_update.value[1]
            self.assertLessEqual(len(text), 35)
