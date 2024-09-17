from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # Redirect to the post's detail view after update
        return reverse('post-detail', kwargs={'pk': self.pk})
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)