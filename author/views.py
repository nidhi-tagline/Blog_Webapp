from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, FormView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .forms import AuthorRegisterForm
from django.contrib.auth import login, views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Author
from .forms import AuthorRegisterForm
from django.http.response import Http404

class BloggerListView(ListView):
    queryset = Author.objects.all()
    template_name = 'author/all_bloggers.html'
    context_object_name = 'authors'
    paginate_by = 10


class BloggerDetailView(DetailView):
    queryset = Author.objects.prefetch_related('blogs')
    template_name = "author/blogger_detail.html"
    context_object_name = "author"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog_list = self.queryset.get(id=self.kwargs['pk']).blogs.order_by('-created_at')

        page_number = self.request.GET.get('page',1)
        page_size = self.request.GET.get('page_size',3)
        paginator = Paginator(blog_list, page_size)
        page_obj = paginator.get_page(page_number)
        context['author_posts'] = page_obj
        return context
        
class AuthorRegisterView(FormView):
    template_name = 'author/register.html'
    form_class = AuthorRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('blog:home')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(AuthorRegisterView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog:home')
        return super(AuthorRegisterView, self).get(*args, **kwargs)
    
class AuthorLoginView(views.LoginView):
    template_name = "author/login.html"
    fields = ['username','password']
    redirect_authenticated_user = True
    success_url = reverse_lazy('blog:home')
    
    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        else:
            return self.success_url
        
class AuthorProfileView(LoginRequiredMixin, DetailView):
    template_name = "author/profile.html"
    queryset = Author.objects.prefetch_related('blogs')
    context_object_name = 'author'
      
    def get_object(self):
        obj = super().get_object()
        if  obj != self.request.user:
            raise Http404
        else:
            return obj
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context['blogs'] = author.blogs.all()
        return context

class AuthorProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "author/profile_update.html"
    fields = ['username','bio_detail']
    queryset = Author.objects.prefetch_related('blogs').all()
    context_object_name = 'author'
    
    # only author can update his profile
    def get_queryset(self):
        queryset = super().get_queryset()
        obj = queryset.filter(id=self.request.user.id)
        if not obj :
            return Http404
        else :
            return obj
        
    def get_success_url(self):
        return reverse("author:author-profile", kwargs={"pk": self.kwargs["pk"],})