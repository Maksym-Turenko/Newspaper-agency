from django.urls import path, include
from django.contrib.auth.views import LogoutView

from news.views import (
    RegisterView,
    NewspaperCreateView,
    NewspaperListView,
    NewspaperDetailView,
    NewspaperUpdateView,
    NewspaperDeleteView,
    LogoutConfirmationView,
    ProfileView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("", NewspaperListView.as_view(), name="index"),
    path("account/register/", RegisterView.as_view(), name="register"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("logout-confirmation/", LogoutConfirmationView.as_view(), name="logout-confirmation"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspaper/create/", NewspaperCreateView.as_view(), name="newspaper-create"),
    path("newspaper/<int:pk>/update/", NewspaperUpdateView.as_view(), name="newspaper-update"),
    path("newspaper/<int:pk>/delete/", NewspaperDeleteView.as_view(), name="newspaper-delete"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit/', UserUpdateView.as_view(), name="user-update"),
    path('profile/delete/', UserDeleteView.as_view(), name="user-delete"),
]
