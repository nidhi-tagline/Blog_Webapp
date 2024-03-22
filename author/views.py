from django.views.generic import ListView, DetailView
from .models import Author
from django.core.paginator import Paginator

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
        