from django.test import TestCase
from django.contrib.auth import get_user_model
from news.forms import (
    RedactorCreationForm,
    NewspaperForm,
    RedactorUpdateForm,
    SearchForm,
)
from news.models import Newspaper, Topic

User = get_user_model()


class RedactorCreationFormTest(TestCase):
    def test_redactor_creation_form_valid(self):
        form_data = {
            "username": "testuser",
            "years_of_experience": 5,
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_redactor_creation_form_invalid_password_mismatch(self):
        form_data = {
            "username": "testuser",
            "years_of_experience": 5,
            "password1": "strongpassword123",
            "password2": "differentpassword456",
        }
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)


class NewspaperFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.topic = Topic.objects.create(name="News")

    def test_newspaper_form_valid(self):
        form_data = {
            "title": "Test Article",
            "content": "Some content",
            "topic": self.topic.id,
            "keywords": "news, update",
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_newspaper_form_invalid_duplicate_title(self):
        Newspaper.objects.create(
            title="Test Article", content="Some content", topic=self.topic
        )
        form_data = {
            "title": "Test Article",
            "content": "Some other content",
            "topic": self.topic.id,
            "keywords": "news, update",
            "publishers": [self.user.id],
        }
        form = NewspaperForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertEqual(
            form.errors["title"], ["An article with this title already exists."]
        )

    def test_newspaper_form_add_user_as_publisher(self):
        form_data = {
            "title": "Another Article",
            "content": "Content here",
            "topic": self.topic.id,
            "keywords": "news, tech",
            "publishers": [],
        }
        form = NewspaperForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        cleaned_publishers = form.clean_publishers()
        self.assertIn(self.user, cleaned_publishers)


class RedactorUpdateFormTest(TestCase):
    def setUp(self):
        self.redactor = User.objects.create_user(
            username="testredactor",
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            years_of_experience=10,
            password="password123",
        )

    def test_redactor_update_form_valid(self):
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "newemail@example.com",
            "years_of_experience": 12,
        }
        form = RedactorUpdateForm(data=form_data, instance=self.redactor)
        self.assertTrue(form.is_valid())

    def test_redactor_update_form_invalid_email_already_exists(self):
        other_redactor = User.objects.create_user(
            username="otheruser", email="existingemail@example.com"
        )
        form_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "existingemail@example.com",
            "years_of_experience": 10,
        }
        form = RedactorUpdateForm(data=form_data, instance=self.redactor)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertEqual(
            form.errors["email"], ["This email address is already in use."]
        )


class SearchFormTest(TestCase):
    def test_search_form_valid(self):
        form_data = {"query": "search term"}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_empty(self):
        form_data = {"query": ""}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["query"], "")
