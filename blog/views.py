from django.views.generic import TemplateView, ListView, DetailView, CreateView
from .models import Blog, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse


class IndexView(TemplateView):
    template_name = "blog/index.html"

class AllBlogView(ListView):
    template_name = "blog/all_blogs.html"
    paginate_by = 5
    context_object_name = 'blog_posts' 
    
    def get_queryset(self):
        return Blog.objects.all().order_by("-created_at")
        
class BlogDetailView(DetailView):
    queryset = Blog.objects.select_related('author')
    template_name = "blog/blog_detail.html"
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_comments'] = self.queryset.get(pk=self.kwargs['pk']).comments.order_by("created_at")
        return context
    
class AddCommentView(LoginRequiredMixin, CreateView):
    template_name = "blog/add_comment.html"
    model = Comment
    fields = ['comment',]
    
    def get_context_data(self, **kwargs):
        context = super(AddCommentView,self).get_context_data(**kwargs)
        context['post'] = Blog.objects.get(pk=self.kwargs['pk'])
        return context
    
    def form_valid(self, form):
        new_comment = form.save(commit=False)
        post = Blog.objects.get(id=self.kwargs["pk"])
        new_comment.created_by = self.request.user
        new_comment.post = post
        new_comment.save(force_insert=True)
        return super().form_valid(form)
    
    def get_success_url(self):  
        return reverse("blog:blog-detail", kwargs={"pk": self.kwargs["pk"],})