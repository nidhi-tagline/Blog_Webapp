from django.urls.conf import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.IndexView.as_view() ,name="home"),
    path('blogs/', views.AllBlogView.as_view(), name='all-blogs'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/comment/', views.AddCommentView.as_view(), name='add-comment'),
    path('blogs/create-blog/', views.CreateBlogView.as_view(), name='create-blog'),
    path('blogs/update/<int:pk>/', views.UpdateBlogView.as_view(), name='update-blog'),
    path('blogs/delete/<int:pk>/', views.DeleteBlogView.as_view(), name= 'delete-blog'),
]
