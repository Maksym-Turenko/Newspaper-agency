from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy

from news.forms import RedactorCreationForm
from news.models import Redactor, Newspaper

def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index/index.html")


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


class NewspaperCreateView(CreateView):
    model = Newspaper
    template_name = 'index/newspaper_create.html'
    fields = ['title', 'content', 'topic', 'publishers', 'keywords']
    success_url = reverse_lazy('index')


class NewspaperListView(ListView):
    model = Newspaper
    template_name = "index/index.html"
    context_object_name = "newspapers"
    paginate_by = 10
