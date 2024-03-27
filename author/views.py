from django.views.generic import ListView, DetailView, FormView
from .models import Author
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import AuthorSignUpForm
from django.contrib.auth import login, views

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
        
class AuthorSignUpView(FormView):
    template_name = 'author/signup.html'
    form_class = AuthorSignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('blog:home')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(AuthorSignUpView, self).form_valid(form)

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