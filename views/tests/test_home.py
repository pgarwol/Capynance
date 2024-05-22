from unittest import TestCase
from views.home import TipsOfTheDay


class TestTipsOfTheDay(TestCase):
    def test_tips_of_the_day(self):
        for tip in self.TipsOfTheDay:
            self.assertTrue(len(tip.value) < 90, f'Tip {tip.name} is too long.')
