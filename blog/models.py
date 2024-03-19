from django.db import models
from author.models import Author
# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __init__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment_description = models.CharField(max_length=300)
    created_by = models.ForeignKey(Author,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)