from django.test import TestCase
from django.core.exceptions import ValidationError

from news.models import Redactor, Topic, Newspaper, Keyword


class RedactorModelTest(TestCase):

    def test_create_redactor(self):
        redactor = Redactor.objects.create_user(username="test_redactor", password="password")
        self.assertEqual(redactor.username, "test_redactor")


class TopicModelTest(TestCase):

    def test_create_topic(self):
        topic = Topic.objects.create(name="test_topic")
        self.assertEqual(topic.name, "test_topic")

    def test_topic_unique_name(self):
        Topic.objects.create(name="Science")
        with self.assertRaises(ValidationError):
            topic = Topic(name="Science")
            topic.full_clean()


class NewspaperModelTest(TestCase):

    def setUp(self):
        self.redactor = Redactor.objects.create_user(username="redactor1", password="password")
        self.topic = Topic.objects.create(name="Science")
        self.keyword1 = Keyword.objects.create(name="Django")
        self.keyword2 = Keyword.objects.create(name="Python")

    def test_create_newspaper(self):
        newspaper = Newspaper.objects.create(
            title="New Discoveries",
            content="Some fascinating content",
            topic=self.topic
        )
        newspaper.publishers.add(self.redactor)
        self.assertEqual(newspaper.title, "New Discoveries")

    def test_newspaper_unique_title_per_redactor(self):
        newspaper1 = Newspaper.objects.create(
            title="AI Breakthrough",
            content="Content about AI",
            topic=self.topic
        )
        newspaper1.publishers.add(self.redactor)

        newspaper2 = Newspaper(
            title="AI Breakthrough",
            content="Another article on AI",
            topic=self.topic
        )
        newspaper2.save()

        newspaper2.publishers.add(self.redactor)

        with self.assertRaises(ValidationError):
            newspaper2.clean()

    def test_keyword_handling_in_newspaper(self):
        newspaper = Newspaper.objects.create(
            title="Tech Innovations",
            content="Content about tech",
            topic=self.topic
        )
        newspaper.publishers.add(self.redactor)
        newspaper.keywords.add(self.keyword1, self.keyword2)

        self.assertEqual(newspaper.keywords.count(), 2)
        self.assertIn(self.keyword1, newspaper.keywords.all())
        self.assertIn(self.keyword2, newspaper.keywords.all())