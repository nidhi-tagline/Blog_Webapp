from django.contrib import admin

from .models import Author
from django.contrib.auth.admin import UserAdmin
from .forms import AuthorChangeForm, AuthorRegisterForm 

class CustomUserAdmin(UserAdmin):
    add_form = AuthorRegisterForm
    form = AuthorChangeForm
    model = Author
    fieldsets = [
        (None, {"fields": ['username','password']}),
        ("Personal info", {"fields": ['bio_detail']}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [(
        None, {
            "classes": ["wide"],
            "fields": ["username", "bio_detail", "password1", "password2"],    
        },
    ),]
    list_display = ["username", "is_active", "is_admin"]
    list_filter = ["username",]
    search_fields = ["username"]
    ordering = ["username"]
    filter_horizontal = []
    
admin.site.register(Author, CustomUserAdmin)
