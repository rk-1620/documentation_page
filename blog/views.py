from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm

class PostListView(ListView):
    model = Post
    template_name = 'blogs/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_form.html'
    success_url = reverse_lazy('Blogsite:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blogs/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blogs/post_form.html'
    success_url = reverse_lazy('Blogsite:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blogs/post_confirm_delete.html'
    success_url = reverse_lazy('Blogsite:post_list')

class CategoryPostListView(ListView):
    model = Post
    template_name = 'blogs/category_post.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

@login_required
def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('Blogsite:post_detail', slug=post.slug)
    else:
        form = CommentForm()
    return render(request, 'blogs/add_comment_to_post.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blogs/category_list.html', {'categories': categories})

def landing_page(request):
    return render(request, 'blogs/landing_page.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Blogsite:landing_page')
    else:
        form = UserCreationForm()
    return render(request, 'blogs/signup.html', {'form': form})

# Profile view function
@login_required
def profile(request):
    return render(request, 'blogs/profile.html', {'user': request.user})

def category_post(request):
    categories = Category.objects.all()
    return render(request, 'blogs/category_post.html', {'categories': categories})
