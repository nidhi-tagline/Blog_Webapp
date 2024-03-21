from django.views import generic
from .models import Author

class BloggerDetailView(generic.DetailView):
    model = Author
    template_name = "author/blogger_detail.html"
    context_object_name = "author"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        context['auth_posts'] = author.blogs.all().order_by('-created_at')
        return context
