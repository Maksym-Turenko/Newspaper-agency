from typing import NoReturn

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.db import transaction


class Redactor(AbstractUser):
    """
    Model representing an editor, inheriting from AbstractUser.
    Added field years_of_experience to store the editor's experience.
    """
    years_of_experience = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="redactor_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="redactor_user_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        return self.username


class Topic(models.Model):
    """
    Model representing a topic of an article.
    """
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Newspaper(models.Model):
    """
    Model representing an article.
    """
    title = models.CharField(max_length=120)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="topic_newspapers"
    )
    publishers = models.ManyToManyField(
        Redactor,
        related_name="redactor_newspapers"
    )
    keywords = models.ManyToManyField(
        "Keyword",
        blank=True,
        related_name="keyword_newspapers"
    )

    class Meta:
        ordering = ["title", "published_date"]

    def clean(self) -> NoReturn:
        """
        Validates that there is no existing article with the same title
        by the same editor. Raises ValidationError if such an article exists.
        """
        super().clean()

        if Newspaper.objects.filter(
                Q(title=self.title) &
                Q(publishers__in=self.publishers.all()) &
                ~Q(id=self.id)
        ).exists():
            raise ValidationError(
                "You already have a newspaper with this title"
            )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to handle keywords.
        """
        keyword_names = [keyword.name for keyword in self.keywords.all()]

        with transaction.atomic():

            super().save(*args, **kwargs)

            existing_keywords = Keyword.objects.filter(name__in=keyword_names)
            existing_keyword_names = set(
                existing_keywords.values_list("name", flat=True)
            )

            new_keywords = [
                Keyword(
                    name=name
                ) for name in keyword_names
                if name not in existing_keyword_names
            ]
            if new_keywords:
                Keyword.objects.bulk_create(new_keywords)

            all_keywords = Keyword.objects.filter(name__in=keyword_names)
            self.keywords.set(all_keywords)

    def __str__(self) -> str:
        return self.title


class Keyword(models.Model):
    """
    Model representing a keyword.
    Each keyword is unique.
    """
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
