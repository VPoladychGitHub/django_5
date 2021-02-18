from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Article, Comment

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'post_status']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text', "username"]
