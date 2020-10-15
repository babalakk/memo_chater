from django.test import TestCase
from .usecase import BaseUsecase
from .models import User, Group, Card, Review


class UsecaseTestCase(TestCase):
    def test_create_user(self):
        user = BaseUsecase.create_user()
        self.assertNotEqual(user, None)

    def test_create_group(self):
        user = User.objects.create()
        group = BaseUsecase.create_group(user.id, "g")
        self.assertEqual(group.name, "g")
        self.assertEqual(group.user_id, user.id)

    def test_create_group_fail(self):
        self.assertRaises(User.DoesNotExist,
                          BaseUsecase.create_group,
                          user_id="fake_user_id",
                          group_name="g")

    def test_create_card(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = BaseUsecase.create_card(group.id, question="q", answer="a")
        self.assertEqual(card.question, "q")
        self.assertEqual(card.answer, "a")
        self.assertEqual(card.group_id, group.id)

    def test_start_review(self):
        user = User.objects.create()
        review = BaseUsecase.start_review(user.id)
        self.assertIsInstance(review, Review)
