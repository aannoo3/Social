from django.shortcuts import get_object_or_404, render
from . models import Post
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . forms import CommentForm

# Create your views here.

# def home(request):
#     posts = Post.objects.all()
#     return render(request, 'blog/base.html', {'posts': posts})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['content', 'image']  # Only the content and image field, but you can add more
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

    def get_queryset(self):
        return Post.objects.all().prefetch_related('likes', 'comments')


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
    
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView
from .models import Post, Comment
from .forms import CommentForm

# ListView for displaying all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/base.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()  # Provide the comment form
        return context

# Like a post
def like_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post-list')  # Redirect back to the home page

# Add a comment to a post
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('post-list')  # Redirect back to the home page

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'  # Default: <app>/<model>_confirm_delete.html
    success_url = reverse_lazy('post-list')  # Redirect to post list after deletion

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
@login_required
def like_unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
