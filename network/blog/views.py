from django.shortcuts import render
from . models import Post
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.urls import reverse
# Create your views here.

# def home(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/base.html', {'posts': posts})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content']  # Only the content field, but you can add more
    template_name = 'blog/post_form.html'  # Reuse the form template

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the post author to the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-list')  # Redirect to the newly created post's detail page

class PostListView(ListView):
    model = Post
    template_name = 'blog/base.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5  # Add pagination (optional)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # Default: <app>/<model>_detail.html
    context_object_name = 'post'


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['content']
    template_name = 'blog/post_form.html'  # Default: <app>/<model>_form.html

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Default: <app>/<model>_confirm_delete.html
    success_url = reverse_lazy('post-list')  # Redirect to post list after deletion

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False