from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Blog, Comment, Author
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse
from django.http.response import Http404

class IndexView(TemplateView):
    template_name = "blog/index.html"

class AllBlogView(ListView):
    template_name = "blog/all_blogs.html"
    paginate_by = 5
    context_object_name = "blog_posts"

    def get_queryset(self):
        return Blog.objects.select_related('author').order_by("-created_at")
        
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

class CreateBlogView(LoginRequiredMixin, CreateView):
    template_name = "blog/create_blog.html"
    model = Blog
    fields = ["title","content"]
    
    def form_valid(self, form):
        new_blog = form.save(commit=False)
        new_blog.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self): 
        return reverse("author:author-profile",kwargs={"pk":self.request.user.id})


class UpdateBlogView(LoginRequiredMixin, UpdateView):
    template_name = "blog/update_blog.html"
    fields = ["title","content"]
    queryset =  Blog.objects.all()

    # only the author of a blog can update it
    def get_queryset(self):
        queryset = super().get_queryset()     
        obj = queryset.filter(author__username=self.request.user.username)
        if not obj:
            raise Http404
        else:
            return obj
    
    def get_success_url(self):
        return reverse("author:author-profile",kwargs={"pk":self.request.user.id})


class DeleteBlogView(LoginRequiredMixin, DeleteView):
    template_name = "blog/delete_blog.html"
    context_object_name = "post"
    queryset =  Blog.objects.all()

    # only the author of a blog can delete it
    def get_queryset(self):
        queryset = super().get_queryset()     
        obj = queryset.filter(author__username=self.request.user.username)
        if not obj:
            raise Http404
        else:
            return obj
        
    def get_success_url(self):
        return reverse("author:author-profile",kwargs={"pk":self.request.user.id})
