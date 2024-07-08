from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CategoryPostListView,
    add_comment_to_post,
    category_list,
    landing_page,
    category_post,
    signup,
    profile
)

app_name = 'Blogsite'

urlpatterns = [
    path('', landing_page, name='landing_page'),  # Landing page
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('categories/', category_list, name='category_list'),
    path('category/<slug:slug>/', CategoryPostListView.as_view(), name='category_post'),
    path('post/<slug:slug>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('login/', auth_views.LoginView.as_view(template_name='blogs/login.html'), name='login'),
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='Blogsite:landing_page'), name='logout'),
]
