from django.db import models
from author.models import Author
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True 

class Blog(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author,on_delete=models.CASCADE)
    
    def __init__(self):
        return self.title
    
class Comment(BaseModel):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    comment_description = models.CharField(max_length=300)
    created_by = models.ForeignKey(Author,on_delete=models.CASCADE)