import uuid
from datetime import date

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Author(models.Model):
    """Model representing an author."""
    class AuthorPrivateStatus(models.IntegerChoices):
        UNPUBLISHED = 1, _('unpublished')  # u
        PUBLISHED = 2, _('published')  # p
    username = models.CharField(_("username"), max_length=100)
    first_name = models.CharField(_("first name"), max_length=100)
    last_name = models.CharField(_("last name"), max_length=100)
    # date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    # mail = models.EmailField(_("mail"), null=True, blank=True)
    # mail_status = models.PositiveSmallIntegerField(choices=AuthorPrivateStatus.choices, default=1)
    # birth_mail_status = models.PositiveSmallIntegerField(choices=AuthorPrivateStatus.choices, default=1)
    class Meta:
        ordering = ['username', 'last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.username}, {self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])


class Comment(models.Model):
    """Model representing a book genre (e.g. Science Fiction, Non Fiction)."""

    class CommentStatus(models.IntegerChoices):
        UNPUBLISHED = 1, _('unpublished')  # u
        PUBLISHED = 2, _('published')  # p

    username = models.CharField(_("username"), max_length=100, default="")
    comment_text = models.TextField(_("comment text"), default="")
    # user = models.ForeignKey(User, verbose_name=_("user"), help_text=_("users commenttt  bio"),
    #                          on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_status = models.PositiveSmallIntegerField(choices=CommentStatus.choices, default=1)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name

    class Meta:
        ordering = ['timestamp', 'comment_text', "username", ]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.comment_text}, {self.timestamp}"


STATUS_CHOICES = (
    ('unpublished', 'UNPUBLISHED'),
    ('published', 'PUBLISHED'),
    ('blanks', 'BLANKS'),
)


class Article(models.Model):
    """Model representing a article ."""
    #
    # class LoanStatus(models.IntegerChoices):
    #     UNPUBLISHED = 1, _('unpublished')  # u
    #     PUBLISHED = 2, _('published')  # p
    #     BLANK = 3, _("blanks")  # b

    title = models.CharField(_("title"), max_length=200)
    body = models.TextField(_("article body"))
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    # status = models.PositiveSmallIntegerField(
    #     choices=LoanStatus.choices, default=LoanStatus.UNPUBLISHED, blank=True, help_text=_('post  unpublished')
    # )
    post_status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='unpublished')

    # @staticmethod
    # def comments(self, pk):
    #     q = Article.objects.get(pk)
    #     return q.comment_set.all()

    def publish(self):
        self.status = 2
        print("def publish(self)")
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ['published_date', 'created_date', 'title', 'author']

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})


class AuthorProfile(models.Model):
    author = models.OneToOneField("Author", on_delete=models.CASCADE)
    about = models.TextField(_("about"), max_length=1000, help_text=_("Author bio"))

    def __str__(self):
        return f"{self.author.last_name} {self.author.first_name} Profile"
