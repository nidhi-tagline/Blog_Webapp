from django.contrib import admin

from .models import Blog, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ['created_by']

class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ['title', 'content']}),
    ]
    inlines =  [CommentInline]
    list_display=['title','author','created_at']
    
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
