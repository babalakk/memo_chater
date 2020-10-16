from django.db import models
from core.tools import uuid4


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=128, default=uuid4)


class Group(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    id = models.CharField(primary_key=True, max_length=128, default=uuid4)
    name = models.CharField(null=False, default="default", max_length=256)


class Card(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    id = models.CharField(primary_key=True, max_length=128, default=uuid4)
    question = models.CharField(null=False, max_length=1024)
    answer = models.CharField(null=False, max_length=1024)
    last_reviewd_at = models.DateTimeField(null=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)

    id = models.CharField(primary_key=True, max_length=128, default=uuid4)
    target_amount = models.IntegerField(null=False)
    current_amount = models.IntegerField(null=False, default=0)
    is_ended = models.BooleanField(default=False)
