from django.db import models
from memo_chater.tools import uuid4


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
    created_at = models.DateTimeField(auto_now_add=True)
    last_review_at = models.DateTimeField(null=True)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    id = models.CharField(primary_key=True, max_length=128, default=uuid4)
    target_amount = models.Integer(null=False)
    current_amount = models.Integer(null=False, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
