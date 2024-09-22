from django.shortcuts import redirect
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

from news.forms import RedactorCreationForm, NewspaperForm
from news.models import Redactor, Newspaper, Keyword


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
        try:
            newspaper = form.save(commit=False)
            newspaper.save()

            keywords = form.cleaned_data.get("keywords", [])
            if keywords:
                for keyword in keywords:
                    keyword_obj, created = Keyword.objects.get_or_create(name=keyword)
                    newspaper.keywords.add(keyword_obj)

            publishers = form.cleaned_data.get("publishers")
            newspaper.publishers.set(publishers)

            messages.success(self.request, "Статья успешно создана!")
            return redirect(self.success_url)

        except Exception as e:
            messages.error(self.request, f"Ошибка при создании статьи: {e}")
            return self.form_invalid(form)



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
        # Сохраняем новую статью
        newspaper = form.save(commit=False)
        new_newspaper = Newspaper.objects.create(
            title=newspaper.title,
            content=newspaper.content,
            topic=newspaper.topic,
            published_date=newspaper.published_date,
        )

        # Обновляем ключевые слова и авторов
        keywords = form.cleaned_data.get("keywords", [])
        for keyword in keywords:
            keyword_obj, created = Keyword.objects.get_or_create(name=keyword)
            new_newspaper.keywords.add(keyword_obj)

        publishers = form.cleaned_data.get("publishers")
        new_newspaper.publishers.set(publishers)

        # Удаляем старую статью
        self.object.delete()

        messages.success(self.request, "Статья успешно обновлена!")
        return redirect(self.success_url)

    def form_invalid(self, form):
        # Если форма не валидна, просто рендерим ее снова
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
    paginate_by = 10


class NewspaperDetailView(LoginRequiredMixin, DetailView):
    model = Newspaper
    template_name = "pages/newspaper_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["is_author"] = self.object.publishers.filter(id=self.request.user.id).exists()
        else:
            context["is_author"] = False
        return context
