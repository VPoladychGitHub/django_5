import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])


class Comment(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""
    body = models.TextField(_("comment body"))
    user = models.ForeignKey(User, verbose_name=_("user"),  help_text=_("users commenttt  bio"), on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        ordering = ['-timestamp', 'body', ]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.body}, {self.timestamp}, {self.user.username}"


class Article(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    title = models.CharField(_("title"), max_length=200)
    body = models.TextField(_("article body"))
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('articles', args=[str(self.id)])


class AuthorProfile(models.Model):
    author = models.OneToOneField("Author", on_delete=models.CASCADE)
    about = models.TextField(_("about"), max_length=1000, help_text=_("Author bio"))

    def __str__(self):
        return f"{self.author.last_name} {self.author.first_name} Profile"
