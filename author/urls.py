from django.urls.conf import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = "author"
urlpatterns = [
    path('', views.BloggerListView.as_view(), name='all-authors'),
    path('<int:pk>/',views.BloggerDetailView.as_view(), name='author-detail'),
    path('<int:pk>/profile/', views.AuthorProfileView.as_view(),name='author-profile'),
    path('<int:pk>/profile/update/', views.AuthorProfileUpdateView.as_view(), name='author-profile-update'),
    path('register/',views.AuthorRegisterView.as_view(), name='register'),
    path('login/', views.AuthorLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='blog:home'), name='logout'),
]
