from django.urls import path, include
from django.contrib.auth.views import LogoutView

from news.views import index, RegisterView, NewspaperCreateView


urlpatterns = [
    path("", index, name="index"),
    path("account/register/", RegisterView.as_view(), name="register"),
    path("logout/", LogoutView.as_view(next_page="index"), name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path('newspaper/create/', NewspaperCreateView.as_view(), name="newspaper-create"),
]
