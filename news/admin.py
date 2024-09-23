from django.contrib import admin, messages

from news.models import Redactor, Topic, Newspaper, Keyword


@admin.register(Redactor)
class RedactorAdmin(admin.ModelAdmin):
    """
    Admin view for Redactor model.
    """

    list_display = (
        "username",
        "first_name",
        "last_name",
        "years_of_experience"
    )
    search_fields = ("username", "first_name", "last_name")
    list_filter = ("years_of_experience", "is_staff", "is_superuser")
    ordering = ("first_name", "last_name")


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
    # """
    # Admin view for Topic model.
    # """
    #
    # list_display = ("name",)
    # search_fields = ("name",)
    # ordering = ("name",)
    #
    # def save_model(self, request, obj, form, change):
    #     obj, created = Topic.objects.get_or_create(name=obj.name)
    #     if created:
    #         super().save_model(request, obj, form, change)
    #     else:
    #         messages.info(request, f'Topic "{obj.name}" уже существует.')


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    """
    Admin view for Newspaper model.
    """

    list_display = ("title", "published_date", "topic")
    search_fields = ("title", "content", "topic__name")
    list_filter = ("published_date", "topic")
    ordering = ("title", "published_date")
    filter_horizontal = ("publishers", "keywords")


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    """
    Admin view for Keyword model.
    """

    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
