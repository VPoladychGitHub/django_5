from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views import generic

from blog.forms import RegisterForm
from blog.models import Article


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


class ArticleListView(generic.ListView):
    """Generic class-based view for a list of cities."""
    model = Article
    paginate_by = 30
