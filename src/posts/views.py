from django.shortcuts import render
from .models import BlogPost
from django.views.generic import CreateView, UpdateView, DetailView,ListView



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