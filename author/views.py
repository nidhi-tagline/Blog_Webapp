from django.views import generic
from .models import Author
from django.core.paginator import Paginator

class BloggerDetailView(generic.DetailView):
    queryset = Author.objects.all()
    template_name = "author/blogger_detail.html"
    context_object_name = "author"
    
    def get_queryset(self):
        return self.queryset.filter(id=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        queryset = author.blogs.order_by('-created_at')        
        paginator = Paginator(queryset, 3)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['author_posts'] = page_obj
        return context
        
    