from django.shortcuts import render
from django.urls import reverse_lazy
from .models import BlogPost
from django.views.generic import CreateView, UpdateView, DetailView,DeleteView,ListView



class BlogHome(ListView):
    model = BlogPost
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        
        return queryset.filter(published=True)


class BlogPostCreate(CreateView):
    model = BlogPost
    template_name = 'posts/blogpost_create.html'
    fields = ['title', 'content', 'published', 'author']
    

class BlogPostUpdate(UpdateView):
    model = BlogPost
    template_name = 'posts/blogpost_edit.html'
    fields = ['title', 'content', 'published' ]


class BlogPostDetail(DetailView):
    model = BlogPost
    template_name = 'posts/blogpost_detail.html'
    context_object_name = 'post'
    field = ['title', 'content' ]

class BlogPostDelete(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('posts:home')
    template_name = 'posts/blogpost_confirm_delete.html'
    context_object_name = 'post'
    field = ['title', 'content' ]