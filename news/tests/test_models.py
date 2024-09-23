from django.test import TestCase
from django.core.exceptions import ValidationError
from news.models import Redactor, Newspaper, Topic, Keyword


class RedactorModelTests(TestCase):

    def setUp(self):
        self.redactor = Redactor.objects.create_user(
            username="editor1", password="password123"
        )
        self.topic = Topic.objects.create(name="Tech")
        self.newspaper = Newspaper.objects.create(
            title="Tech News", content="Content about tech", topic=self.topic
        )
        self.newspaper.publishers.add(self.redactor)

    def test_delete_redactor_deletes_related_newspapers(self):
        """
        Ensure that when a redactor is deleted, all related newspapers are also deleted.
        """
        self.redactor.delete()

        # Ensure that the newspaper is deleted as well since the redactor was the only publisher
        self.assertFalse(Newspaper.objects.filter(title="Tech News").exists())

    def test_redactor_str(self):
        """
        Test the string representation of the Redactor model.
        """
        self.assertEqual(str(self.redactor), "editor1")


class NewspaperModelTests(TestCase):

    def setUp(self):
        self.topic = Topic.objects.create(name="Politics")
        self.redactor = Redactor.objects.create_user(
            username="editor2", password="password123"
        )

    def test_newspaper_unique_title_validation(self):
        """
        Ensure that a ValidationError is raised if a newspaper with the same title already exists.
        """
        Newspaper.objects.create(
            title="Breaking News", content="Some content", topic=self.topic
        )

        # Try to create another newspaper with the same title, expecting ValidationError
        newspaper = Newspaper(
            title="Breaking News", content="Another content", topic=self.topic
        )
        with self.assertRaises(ValidationError):
            newspaper.clean()

    def test_keyword_creation(self):
        """
        Ensure that keywords are correctly created and linked to a newspaper.
        """
        newspaper = Newspaper.objects.create(
            title="Sports News", content="Some sports content", topic=self.topic
        )
        newspaper.publishers.add(self.redactor)
        keyword1 = Keyword.objects.create(name="Football")
        keyword2 = Keyword.objects.create(name="Championship")
        newspaper.keywords.add(keyword1, keyword2)

        # Ensure that the keywords are correctly linked to the newspaper
        self.assertSetEqual(
            set(newspaper.keywords.values_list("name", flat=True)),
            {"Football", "Championship"},
        )
