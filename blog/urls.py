from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.IndexView.as_view() ,name="home"),
    path('blogs/', views.AllBlogView.as_view(), name='all-blogs'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('blogs/<int:pk>/create/', views.AddCommentView.as_view(), name='add-comment')
]
