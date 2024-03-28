
from django.contrib import admin
from django.urls.conf import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include("blog.urls")),
    path('blogs/bloggers/', include("author.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
]
