from django.contrib import admin

# Register your models here.
from .models import BlogItemModel


class BlogItemModelAdmin(admin.ModelAdmin):
    list_display = ["title", "updated", "created"]
    list_filter = ["updated", "created"]
    search_fields = ["title", "content"]

    class Meta:
        model = BlogItemModel



admin.site.register(BlogItemModel, BlogItemModelAdmin)
