from .models import User, Group, Card, Review
from datetime import datetime


class BaseUsecase:
    def create_user():
        user = User.objects.create()
        return user

    def create_group(user_id, group_name):
        if Group.objects.filter(user_id=user_id, name=group_name).first():
            raise Exception("group name already exists")
        return Group.objects.create(user_id=user_id, name=group_name)

    def create_card(group_id, question, answer):
        card = Card.objects.create(group_id=group_id, question=question, answer=answer)
        return card

    @classmethod
    def start_review(cls, group_id, target_amount=20):
        group = Group.objects.get(pk=group_id)
        if cls.get_current_review(group.user_id):
            raise Exception("unfinished review exists")
        review = Review.objects.create(user_id=group.user_id, group=group, target_amount=target_amount)
        return review

    def get_current_review(user_id):
        return Review.objects.filter(user_id=user_id, is_ended=False).first()

    def end_review(review_id):
        Review.objects.filter(pk=review_id).update(is_ended=True)

    @classmethod
    def pick_question(cls, review_id):
        review = Review.objects.get(pk=review_id)
        card = cls.__choose_card(review.group_id)
        review.card = card
        review.save()
        return card.question

    def __choose_card(group_id):
        card = Card.objects.filter(group_id=group_id).order_by("last_reviewd_at").first()
        return card

    def get_answer(review_id):
        review = Review.objects.get(pk=review_id)
        card = Card.objects.get(pk=review.card_id)
        return card.answer

    @classmethod
    def answer_review_question_and_pick_next(cls, review_id, value):
        review = Review.objects.get(pk=review_id)
        Card.objects.filter(pk=review.card_id).update(last_reviewd_at=datetime.utcnow())

        review.current_amount = review.current_amount+1
        review.save()

        if review.current_amount >= review.target_amount:
            cls.end_review(review.id)
        else:
            return cls.pick_question(review.id)
