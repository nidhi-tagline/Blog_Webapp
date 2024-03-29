from django.db import models
from author.models import Author
from django.conf import settings

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract=True 

class Blog(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs')
    
    def __str__(self):
        return self.title
    
class Comment(BaseModel):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=300)
    created_by = models.ForeignKey(Author,on_delete=models.CASCADE , related_name= 'commentor')
    
    def __str__(self):
        if len(self.comment) > settings.TRUNCATE_CHAR_LIMIT:
            return self.comment[:40] + "..."  
        else:
            return self.comment