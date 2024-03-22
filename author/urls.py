from django.urls import path
from . import views

app_name = "author"
urlpatterns = [
    path('<int:pk>/',views.BloggerDetailView.as_view(), name='author-detail')
]
