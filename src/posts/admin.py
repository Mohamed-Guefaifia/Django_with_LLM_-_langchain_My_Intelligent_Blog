from django.contrib import admin

# Register your models here.
from .models import BlogPost  



class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','published','created_on','last_updated')
    list_filter = ('published','author')
   

admin.site.register(BlogPost,BlogPostAdmin)