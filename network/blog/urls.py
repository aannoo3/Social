from django.urls import path
from .views import PostListView, PostDetailView, PostUpdateView, PostDeleteView, PostCreateView, like_post, add_comment

urlpatterns = [
    path('post/new/', PostCreateView.as_view(), name='post-create'),  # Create new post
    path('', PostListView.as_view(), name='post-list'),  # List of posts
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # Single post detail
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),  # Update post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # Delete post
    path('like/<int:pk>/', like_post, name='like-post'),
    path('comment/<post_id>/', add_comment, name='add-comment'),


]
