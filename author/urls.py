from django.urls import path
from . import views

app_name = "author"
urlpatterns = [
    path('', views.BloggerListView.as_view(), name='all-authors'),
    path('<int:pk>/',views.BloggerDetailView.as_view(), name='author-detail'),
]
