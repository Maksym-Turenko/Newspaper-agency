from typing import NoReturn

from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.utils.timezone import now
from news.admin import RedactorAdmin, TopicAdmin, NewspaperAdmin, KeywordAdmin

from news.models import Redactor, Topic, Newspaper, Keyword


class MockRequest:
    pass


class RedactorAdminTest(TestCase):
    def setUp(self) -> NoReturn:
        self.site = AdminSite()
        self.redactor_admin = RedactorAdmin(Redactor, self.site)
        self.redactor = Redactor.objects.create_user(
            username="test_redactor",
            first_name="Test",
            last_name="Redactor",
            years_of_experience=5,
            password="testpassword123"
        )

    def test_list_display(self) -> NoReturn:
        self.assertEqual(
            list(self.redactor_admin.get_list_display(MockRequest())),
            ["username", "first_name", "last_name", "years_of_experience"]
        )

    def test_search_fields(self) -> NoReturn:
        self.assertEqual(
            self.redactor_admin.get_search_fields(MockRequest()),
            ("username", "first_name", "last_name")
        )

    def test_list_filter(self) -> NoReturn:
        self.assertEqual(
            self.redactor_admin.get_list_filter(MockRequest()),
            ("years_of_experience", "is_staff", "is_superuser")
        )


class TopicAdminTest(TestCase):
    def setUp(self) -> NoReturn:
        self.site = AdminSite()
        self.topic_admin = TopicAdmin(Topic, self.site)
        self.topic = Topic.objects.create(name="Sports")

    def test_list_display(self) -> NoReturn:
        self.assertEqual(
            list(self.topic_admin.get_list_display(MockRequest())),
            ["name"]
        )

    def test_search_fields(self) -> NoReturn:
        self.assertEqual(
            self.topic_admin.get_search_fields(MockRequest()),
            ("name",)
        )

    def test_ordering(self) -> NoReturn:
        self.assertEqual(
            self.topic_admin.get_ordering(MockRequest()),
            ("name",)
        )


class NewspaperAdminTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.newspaper_admin = NewspaperAdmin(Newspaper, self.site)
        self.topic = Topic.objects.create(name="Technology")
        self.redactor = Redactor.objects.create_user(
            username="editor1",
            first_name="John",
            last_name="Doe",
            password="editorpassword"
        )
        self.keyword = Keyword.objects.create(name="Innovation")

        self.newspaper = Newspaper.objects.create(
            title="Tech News",
            content="New tech releases this week.",
            topic=self.topic,
            published_date=now().date()
        )

        self.newspaper.publishers.add(self.redactor)
        self.newspaper.keywords.add(self.keyword)

    def test_list_display(self) -> NoReturn:
        self.assertEqual(
            list(self.newspaper_admin.get_list_display(MockRequest())),
            ["title", "published_date", "topic"]
        )

    def test_search_fields(self) -> NoReturn:
        self.assertEqual(
            self.newspaper_admin.get_search_fields(MockRequest()),
            ("title", "content", "topic__name")
        )

    def test_list_filter(self) -> NoReturn:
        self.assertEqual(
            self.newspaper_admin.get_list_filter(MockRequest()),
            ("published_date", "topic")
        )

    def test_filter_horizontal(self) -> NoReturn:
        self.assertEqual(
            self.newspaper_admin.filter_horizontal,
            ("publishers", "keywords")
        )


class KeywordAdminTest(TestCase):
    def setUp(self) -> NoReturn:
        self.site = AdminSite()
        self.keyword_admin = KeywordAdmin(Keyword, self.site)
        self.keyword = Keyword.objects.create(name="AI")

    def test_list_display(self) -> NoReturn:
        self.assertEqual(
            list(self.keyword_admin.get_list_display(MockRequest())),
            ["name"]
        )

    def test_search_fields(self) -> NoReturn:
        self.assertEqual(
            self.keyword_admin.get_search_fields(MockRequest()),
            ("name",)
        )

    def test_ordering(self) -> NoReturn:
        self.assertEqual(
            self.keyword_admin.get_ordering(MockRequest()),
            ("name",)
        )
