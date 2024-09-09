from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        # Redirect to the post's detail view after update
        return reverse('post-detail', kwargs={'pk': self.pk})