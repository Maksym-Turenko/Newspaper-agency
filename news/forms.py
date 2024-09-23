from django.contrib.auth.forms import UserCreationForm
from news.models import Newspaper, Redactor
from django import forms


class RedactorCreationForm(UserCreationForm):
    class Meta:
        model = Redactor
        fields = ["username", "years_of_experience", "password1", "password2"]


class NewspaperForm(forms.ModelForm):
    keywords = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Enter keywords separated by commas"}
        ),
        help_text="Add keywords separated by commas",
    )
    publishers = forms.ModelMultipleChoiceField(
        queryset=Redactor.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        required=False,
        help_text="Add other authors if needed",
    )

    class Meta:
        model = Newspaper
        fields = ["title", "content", "topic", "publishers", "keywords"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.initial["keywords"] = ", ".join(
                keyword.name for keyword in self.instance.keywords.all()
            )

    def clean_title(self):
        title = self.cleaned_data.get("title")
        if self.instance and self.instance.title == title:
            return title

        if Newspaper.objects.filter(title=title).exists():
            raise forms.ValidationError(
                "An article with this title already exists."
            )
        return title

    def clean_keywords(self):
        keywords = self.cleaned_data["keywords"]
        keyword_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        return keyword_list

    def clean_publishers(self):
        publishers = self.cleaned_data.get("publishers", [])
        if self.user and self.user not in publishers:
            publishers = list(publishers)
            publishers.append(self.user)
        return publishers


class RedactorUpdateForm(forms.ModelForm):
    class Meta:
        model = Redactor
        fields = ["first_name", "last_name", "email", "years_of_experience"]
        widgets = {
            "email": forms.EmailInput(attrs={"required": "required"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Redactor.objects.exclude(
                pk=self.instance.pk
        ).filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use."
            )
        return email


class SearchForm(forms.ModelForm):
    query = forms.CharField(
        label="Search",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title, author, or keywords...",
                "style": "width: 700px;",
            }
        ),
        required=False,
    )

    class Meta:
        model = Newspaper
        fields = ["query"]
