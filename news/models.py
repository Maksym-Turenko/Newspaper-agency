from django.db import models
from django.contrib.auth.models import AbstractUser


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.username


class Topic(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="topic_newspapers"
    )
    publisher = models.ManyToManyField(Redactor, related_name="redactor_newspapers")
