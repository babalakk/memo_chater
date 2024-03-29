from django.conf import settings
from pymessenger.bot import Bot
from apps.core.models import User, Group, Card, Review
from apps.core.usecase import ManageUsecase, ReviewUsecase

bot = Bot(settings.FB_PAGE_TOKEN)


CMD_SHOW_GROUP = "showgroup"
CMD_CREATE_GROUP = "addgroup"
CMD_DELETE_GROUP = "delgroup"
CMD_ADD_CARD = "addcard"
CMD_DELETE_CARD = "delcard"
CMD_REVIEW_GROUP = "review"
CMD_SHOW_ANSWER = "showanswer"
CMD_EVALUATE = "evaluate"


def button(text, title=None):
    return {
        "type": "postback",
        "payload": text,
        "title": title or text
    }


class Chater:
    def show_menu(user):
        bot.send_button_message(
            recipient_id=user.fb_id,
            text="Memo Chater",
            buttons=[button(text=CMD_SHOW_GROUP, title="Start Review")])

    def show_groups(user):
        groups = Group.objects.filter(user_id=user.id).all()
        if groups:
            group_name_buttons = [button(text=f"{CMD_REVIEW_GROUP} {g.name}", title=g.name) for g in groups]
            bot.send_button_message(
                recipient_id=user.fb_id,
                text="Choose a group to review.",
                buttons=group_name_buttons
            )
        else:
            bot.send_text_message(
                recipient_id=user.fb_id,
                message=f"You don't have card group yet. Type '{CMD_CREATE_GROUP} [group_name]' to create new group.")

    def create_group(user, params):
        group = ManageUsecase.create_group(user.id, params[0])
        bot.send_text_message(
            recipient_id=user.fb_id, message=f"Group '{group.name}' created. Type '{CMD_ADD_CARD} {group.name} [question] [answer]' to create new card.")

    def delete_group(user, params):
        Group.objects.filter(user_id=user.id, name=params[0]).delete()
        bot.send_text_message(recipient_id=user.fb_id, message=f"Group '{params[0]}' deleted.")

    def add_card(user, params):
        group = Group.objects.filter(user_id=user.id, name=params[0]).first()
        Card.objects.create(group_id=group.id, question=params[1], answer=params[2])
        bot.send_text_message(recipient_id=user.fb_id, message=f"Card created.")

    def delete_card(user, params):
        group = Group.objects.filter(user_id=user.id, name=params[0]).first()
        card = Card.objects.filter(group_id=group.id, question=params[1]).first()
        if card:
            ManageUsecase.delete_card(card.id)
        bot.send_text_message(recipient_id=user.fb_id, message=f"Card deleted.")

    @classmethod
    def review_group(cls, user, params):
        group = Group.objects.filter(user_id=user.id, name=params[0]).first()
        review = ReviewUsecase.start_review(group, target_amount=3)
        question = ReviewUsecase.pick_question(review)
        if not question:
            bot.send_text_message(
                recipient_id=user.fb_id, message=f"Group '{group.name}' does not have card yet. Type '{CMD_ADD_CARD} {group.name} [question] [answer]' to create new card.")
        cls.show_question(user.fb_id, question, review.id)

    def show_question(recipient_id, question, review_id):
        bot.send_button_message(
            recipient_id=recipient_id,
            text=question,
            buttons=[
                button(title="Show Answer", text=f"{CMD_SHOW_ANSWER} {review_id}")])

    def show_answer(user, params):
        review = Review.objects.filter(id=params[0], user_id=user.id).first()
        answer = ReviewUsecase.get_answer(review)
        bot.send_button_message(
            recipient_id=user.fb_id,
            text=answer,
            buttons=[
                button(title="Good", text=f"{CMD_EVALUATE} {review.id} 1"),
                button(title="Bad", text=f"{CMD_EVALUATE} {review.id} 0")
            ]
        )

    @classmethod
    def evaluate(cls, user, params):
        review = Review.objects.filter(id=params[0], user_id=user.id).first()
        question = ReviewUsecase.evaluate_and_pick_next_question(review, params[1])
        if question:
            cls.show_question(user.fb_id, question, review.id)
        else:
            bot.send_text_message(recipient_id=user.fb_id, message=f"Review finished.")
            cls.show_menu(user)

    @classmethod
    def chat(cls, recipient_id, text):
        user, _ = User.objects.get_or_create(fb_id=recipient_id)
        command, params = cls.__get_input(text)
        if command == CMD_SHOW_GROUP:
            cls.show_groups(user)
        elif command == CMD_CREATE_GROUP:
            cls.create_group(user, params)
        elif command == CMD_DELETE_GROUP:
            cls.delete_group(user, params)
        elif command == CMD_ADD_CARD:
            cls.add_card(user, params)
        elif command == CMD_REVIEW_GROUP:
            cls.review_group(user, params)
        elif command == CMD_SHOW_ANSWER:
            cls.show_answer(user, params)
        elif command == CMD_EVALUATE:
            cls.evaluate(user, params)
        elif command == CMD_DELETE_CARD:
            cls.delete_card(user, params)
        else:
            cls.show_menu(user)

    def __get_input(text):
        inputs = text.split(" ")
        if len(inputs) >= 2:
            return inputs[0], inputs[1:]
        else:
            return inputs[0], []
