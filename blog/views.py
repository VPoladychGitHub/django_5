from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.views.generic import CreateView

from django.contrib.auth import authenticate, login

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic

from blog.forms import RegisterForm, ArticleForm, CommentForm
from blog.models import Article, Author


def index(request):
    return HttpResponse("Hello, world. You're at the blog index.")


def index2(request):
    context = {}
    return TemplateResponse(request, "blog/article_list.html", context=context)


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


def view_user(request, username):
    un = request.user.username
    auther_queryset = Author.objects.all()
    if auther_queryset.filter(username=username).exists():
        print("User contained in queryset")
        author = Author.objects.get(username=username)
        return redirect('author-update', pk=author.pk)
    else:
        print("User not  contained in queryset  you mast relogin: " + username)
        return redirect('article_list')


class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


# class AuthorUpdate(PermissionRequiredMixin, generic.UpdateView):
class AuthorUpdate(generic.UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth']


class ArticleListView(generic.ListView):
    """Generic class-based view for a list of cities."""
    model = Article
    paginate_by = 30


class ArticleDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Article
    fields = ['title', 'body', 'author', 'created_date', 'post_status']


class ArticleCreate(generic.CreateView):
    model = Article
    fields = ['title', 'body', 'author', 'created_date', 'post_status']
    initial = {'post_status': 'unpublished'}


# def article_list(request):
#     un = request.user.username
#     print("user : " + str(un))
#     user = Author.objects.get(username=un)
#     article_list = user.article_set.all()
#
#     paginator = Paginator(article_list, 10)  # Show 30 contacts per page.
#
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'blog/article_list.html', {'page_obj': page_obj})


def article_list_by_user(request):
    # un = request.user.username
    # i = Author.objects.get(username__contains=un)
    # print("user : " + str(un))
    # i = Author.objects.get(username__contains=un)
    # print('username__contains ============================== ' + str(i))
    un = request.user.username
    auther_queryset = Author.objects.all()
    if auther_queryset.filter(username=un).exists():
        print("Entry contained in queryset")
        user = Author.objects.get(username=un)
        article_list = user.article_set.all()

        paginator = Paginator(article_list, 10)  # Show 30 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/article_list.html', {'page_obj': page_obj})
    else:
        return redirect('article_list')


def article_detail(request, pk):
    article = Article.objects.get(pk=pk)
    comments = list(article.comment_set.all())
    path_post = request.scheme + '://' + request.get_host() + request.path

    request.session['path_post'] = path_post
    return render(request, 'blog/article_detail2.html',
                  {'article': article, 'pk': pk, "comments": comments, "author": str(article.author.username),
                   'path_post': path_post})


def article_new(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            ru = request.user.username
            a = form.cleaned_data['author']
            print(a.username)
            print(ru)
            if ru != a.username:
                print('Invalid username auther not same logged user:   ' + a.username + "  " + ru)
                messages.add_message(request, messages.ERROR,
                                     'Invalid username auther not same logged user:' + a.username)
                # value = "Invalid username auther not same logged user"
                # raise ValidationError(_('Invalid username auther not same logged user: %(value)s'),
                #                       code='invalid',
                #                       params={'value': value}, )
            else:
                print(form.cleaned_data['post_status'])
                f.author = a
                ps = form.cleaned_data['post_status']
                if ps == 'published':
                    f.published_date = timezone.now()
                f.save()
                send_mail('subject', "new post", 'admin@example.com', [a.mail])
                return redirect('article-detail', pk=f.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/article_edit.html', {'form': form})


def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            f = form.save(commit=False)
            ru = request.user.username
            a = form.cleaned_data['author']
            print(a.username)
            print(ru)
            if ru != a.username:
                messages.add_message(request, messages.ERROR,
                                     'Invalid username auther not same logged user:' + a.username)

                # value = a
                # raise ValidationError(_('Invalid username auther not same logged user: %(value)s'),
                #                       code='invalid',
                #                       params={'value': value}, )
            else:
                f.author = a
                ps = form.cleaned_data['post_status']
                if ps == 'published':
                    f.published_date = timezone.now()
                f.save()
                return redirect('article-detail', pk=f.pk)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_edit.html', {'form': form, 'pk': article.pk})


# def comment_new(request, pk, path):
def comment_new(request, pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.article_id = pk
            f.timestamp = timezone.now()
            f.save()

            path_post = request.session['path_post']
         #   print("path_post  :" + str(f.article.author.mail))
            send_mail('subject', path_post, 'admin@example.com', [f.article.author.mail])
            return redirect('article-detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_new.html', {'form': form, 'pk': pk})
