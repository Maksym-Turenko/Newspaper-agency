from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from news.forms import (
    RedactorCreationForm,
    NewspaperForm,
    RedactorUpdateForm,
    SearchForm,
)
from news.models import (
    Redactor,
    Newspaper,
    Keyword,
)


class RegisterView(CreateView):
    model = Redactor
    form_class = RedactorCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class LogoutConfirmationView(TemplateView):
    template_name = "registration/logout.html"

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')


class NewspaperCreateView(LoginRequiredMixin, CreateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "forms/create_forms/newspaper_create.html"
    success_url = reverse_lazy("index")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.save()

        keywords = form.cleaned_data.get("keywords", [])
        if keywords:
            keyword_objs = [Keyword.objects.get_or_create(name=keyword)[0] for keyword in keywords]
            newspaper.keywords.add(*keyword_objs)

        publishers = form.cleaned_data.get("publishers")
        newspaper.publishers.set(publishers)

        messages.success(self.request, "Article successfully created!")
        return redirect(self.success_url)


class NewspaperUpdateView(LoginRequiredMixin, UpdateView):
    model = Newspaper
    form_class = NewspaperForm
    template_name = "forms/update_forms/newspaper_update.html"
    success_url = reverse_lazy("index")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publishers=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        new_newspaper = Newspaper.objects.create(
            title=newspaper.title,
            content=newspaper.content,
            topic=newspaper.topic,
            published_date=newspaper.published_date,
        )

        keywords = form.cleaned_data.get("keywords", [])
        for keyword in keywords:
            keyword_obj, created = Keyword.objects.get_or_create(name=keyword)
            new_newspaper.keywords.add(keyword_obj)

        publishers = form.cleaned_data.get("publishers")
        new_newspaper.publishers.set(publishers)

        self.object.delete()

        messages.success(self.request, "Статья успешно обновлена!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response({'form': form})


class NewspaperDeleteView(LoginRequiredMixin, DeleteView):
    model = Newspaper
    template_name = "forms/delete_forms/newspaper_confirm_delete.html"
    success_url = reverse_lazy("index")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(publishers=self.request.user)


class NewspaperListView(ListView):
    model = Newspaper
    template_name = "pages/index.html"
    context_object_name = "newspapers"
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related("topic")
        queryset = queryset.prefetch_related("publishers", "keywords")
        category = self.request.GET.get("category")
        query = self.request.GET.get("query")

        if category:
            queryset = queryset.filter(topic__name__iexact=category)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(publishers__first_name__icontains=query) |
                Q(publishers__last_name__icontains=query) |
                Q(keywords__name__icontains=query)
            ).distinct()

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm(self.request.GET)
        return context


class NewspaperDetailView(LoginRequiredMixin, DetailView):
    model = Newspaper
    template_name = "pages/newspaper_detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("publishers")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_author"] = self.object.publishers.filter(id=self.request.user.id).exists()
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "pages/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Redactor
    form_class = RedactorUpdateForm
    template_name = "forms/update_forms/user_update_form.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return get_object_or_404(Redactor, id=self.request.user.id)

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error.")
        return super().form_invalid(form)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = Redactor
    template_name = "forms/delete_forms/user_delete_form.html"
    success_url = reverse_lazy("index")

    def get_object(self, queryset=None):
        return get_object_or_404(Redactor, id=self.request.user.id)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your profile has been deleted!")
        return super().delete(request, *args, **kwargs)


class UserArticlesListView(LoginRequiredMixin, ListView):
    model = Newspaper
    template_name = "pages/users_articles.html"
    context_object_name = "user_newspapers"
    paginate_by = 5

    def get_queryset(self):
        return Newspaper.objects.filter(publishers=self.request.user).distinct()
