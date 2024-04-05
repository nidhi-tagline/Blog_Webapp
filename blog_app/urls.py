from django.contrib import admin
from django.urls.conf import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include("blog.urls")),
    path('blogs/bloggers/', include("author.urls")),
]

if settings.DEBUG_TOOLBAR :
    urlpatterns += [
        path('__debug__/', include("debug_toolbar.urls")),
    ]