from django.shortcuts import render
from . models import Post
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
# Create your views here.

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/base.html', {'posts': posts})


class PostListView(ListView):
    model = Post
    template_name = 'blog/base.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']