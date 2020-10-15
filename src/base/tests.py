from django.test import TestCase
from .usecase import BaseUsecase
from .models import User, Group, Card, Review


class UsecaseTestCase(TestCase):
    def test_create_user(self):
        user = BaseUsecase.create_user()
        self.assertIsInstance(user, User)

    def test_create_group(self):
        user = User.objects.create()
        group = BaseUsecase.create_group(user.id, "g")
        self.assertEqual(group.name, "g")
        self.assertEqual(group.user_id, user.id)

    def test_create_card(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = BaseUsecase.create_card(group.id, question="q", answer="a")
        self.assertEqual(card.question, "q")
        self.assertEqual(card.answer, "a")
        self.assertEqual(card.group_id, group.id)

    def test_start_review(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        review = BaseUsecase.start_review(group.id, 30)
        self.assertIsInstance(review, Review)
        self.assertEqual(review.target_amount, 30)

    def test_pick_question(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        Card.objects.create(group=group, question="q", answer="a")
        review = Review.objects.create(user=user, group=group, target_amount=30)
        question = BaseUsecase.pick_question(review.id)
        self.assertEqual(question, "q")

    def test_answer_review_question_and_pick_next(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = Card.objects.create(group=group, question="q", answer="a")
        review = Review.objects.create(user=user, group=group, target_amount=30, card=card)
        question = BaseUsecase.answer_review_question_and_pick_next(review.id, 123)
        self.assertEqual(question, "q")

        review.refresh_from_db()
        self.assertEqual(review.current_amount, 1)

    def test_review_pick_until_finish(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = Card.objects.create(group=group, question="q", answer="a")
        review = Review.objects.create(user=user, group=group, target_amount=2, card=card)
        BaseUsecase.answer_review_question_and_pick_next(review.id, 123)
        question = BaseUsecase.answer_review_question_and_pick_next(review.id, 123)
        self.assertEqual(question, None)
