from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.TextField()
    description = models.TextField()
    publish_date = models.TextField()
    author = models.TextField()
    
    def __str__(self):
        return self.title 

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"