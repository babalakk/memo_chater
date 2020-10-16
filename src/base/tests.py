from django.test import TestCase
from .usecase import ManageUsecase, ReviewUsecase
from .models import User, Group, Card, Review
from datetime import datetime, timedelta


class BaseUsecaseTestCase(TestCase):
    def test_create_user(self):
        user = ManageUsecase.create_user()
        self.assertIsInstance(user, User)

    def test_create_group(self):
        user = User.objects.create()
        group = ManageUsecase.create_group(user.id, "g")
        self.assertEqual(group.name, "g")
        self.assertEqual(group.user_id, user.id)

    def test_create_card(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = ManageUsecase.create_card(group.id, question="q", answer="a")
        self.assertEqual(card.question, "q")
        self.assertEqual(card.answer, "a")
        self.assertEqual(card.group_id, group.id)


class ReviewUsecaseTestCase(TestCase):
    def test_start_review(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        review = ReviewUsecase.start_review(group, 30)
        self.assertIsInstance(review, Review)
        self.assertEqual(review.target_amount, 30)

    def test_pick_question(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        Card.objects.create(group=group, question="q", answer="a")
        review = Review.objects.create(user=user, group=group, target_amount=30)
        question = ReviewUsecase.pick_question(review)
        self.assertEqual(question, "q")

    def test_evaluate_and_pick_next_question(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = Card.objects.create(group=group, question="q", answer="a")
        review = Review.objects.create(user=user, group=group, target_amount=30, card=card)
        question = ReviewUsecase.evaluate_and_pick_next_question(review, 123)
        self.assertEqual(question, "q")

        review.refresh_from_db()
        self.assertEqual(review.current_amount, 1)

    def test_review_pick_until_finish(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        card = Card.objects.create(group=group, question="q", answer="a")
        review = Review.objects.create(user=user, group=group, target_amount=2, card=card)
        ReviewUsecase.evaluate_and_pick_next_question(review, 123)
        question = ReviewUsecase.evaluate_and_pick_next_question(review, 123)
        self.assertEqual(question, None)

    def test_pick_older_card(self):
        user = User.objects.create()
        group = Group.objects.create(user=user)
        Card.objects.create(group=group, question="q1", answer="a2", last_reviewd_at=datetime.utcnow())
        Card.objects.create(group=group, question="q2", answer="a2",
                            last_reviewd_at=datetime.utcnow()-timedelta(days=1))
        review = Review.objects.create(user=user, group=group, target_amount=30)
        question = ReviewUsecase.pick_question(review)
        self.assertEqual(question, "q2")
