from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from news.models import Redactor, Newspaper, Topic, Keyword
from news.forms import SearchForm

User = get_user_model()


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")

    def test_register_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_register_view_post(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "password1": "password1234",
                "password2": "password1234",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


class LogoutConfirmationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")

    def test_logout_view_post(self):
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("index"))
        self.assertNotIn("_auth_user_id", self.client.session)


class NewspaperCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.topic = Topic.objects.create(name="Politics")
        self.url = reverse("newspaper-create")

    def test_create_newspaper(self):
        form_data = {
            "title": "New Title",
            "content": "New Content",
            "keywords": "news, updates",
        }
        response = self.client.post(reverse("newspaper:create"), data=form_data)
        newspaper = Newspaper.objects.get(title="New Title")
        self.assertTrue(newspaper.keywords.filter(name="news").exists())


class NewspaperUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.topic = Topic.objects.create(name="Politics")
        self.newspaper = Newspaper.objects.create(
            title="Old Title", content="Old content", topic=self.topic
        )
        self.newspaper.publishers.add(self.user)
        self.url = reverse("newspaper-update", kwargs={"pk": self.newspaper.pk})

    def test_update_newspaper(self):
        response = self.client.post(
            self.url,
            {
                "title": "Updated Title",
                "content": "Updated content",
                "topic": self.topic.id,
                "keywords": ["update", "news"],
                "publishers": [self.user.id],
            },
        )
        self.assertRedirects(response, reverse("index"))
        self.assertTrue(Newspaper.objects.filter(title="Updated Title").exists())
        self.assertFalse(Newspaper.objects.filter(title="Old Title").exists())


class NewspaperListViewTest(TestCase):
    def setUp(self):
        self.newspaper1 = Newspaper.objects.create(
            title="Tech News", content="Tech content"
        )
        self.newspaper2 = Newspaper.objects.create(
            title="Art News", content="Art content"
        )

        self.url = reverse("newspaper-list")

    def test_list_view_with_filter(self):
        response = self.client.get(self.url, {"query": "Tech"})
        self.assertContains(response, self.newspaper1.title)
        self.assertNotContains(response, self.newspaper2.title)


class UserArticlesListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.login(username="testuser", password="password123")
        self.other_user = User.objects.create_user(
            username="otheruser", password="password123"
        )
        self.newspaper1 = Newspaper.objects.create(
            title="User's News", content="Content"
        )
        self.newspaper1.publishers.add(self.user)
        self.newspaper2 = Newspaper.objects.create(
            title="Other's News", content="Content"
        )
        self.newspaper2.publishers.add(self.other_user)
