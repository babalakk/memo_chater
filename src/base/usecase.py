from .models import User, Group, Card


class BaseUsecase:
    def create_user():
        user = User.objects.create()
        return user

    def create_group(user_id, group_name):
        user = User.objects.get(pk=user_id)
        return Group.objects.create(user=user, name=group_name)

    def create_card(group_id, question, answer):
        group = Group.objects.get(pk=group_id)
        card = Card.objects.create(group=group, question=question, answer=answer)
        return card
