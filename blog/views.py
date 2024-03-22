from django.views import generic
from .models import Blog, Comment


class IndexView(generic.TemplateView):
    template_name = "blog/index.html"

class AllBlogView(generic.ListView):
    template_name = "blog/all_blogs.html"
    paginate_by = 5
    context_object_name = 'blog_posts' 
    
    def get_queryset(self):
        return Blog.objects.all().order_by("-created_at")
        