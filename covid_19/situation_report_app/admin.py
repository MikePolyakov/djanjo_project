from django.contrib import admin
from .models import Article, Place, Post, Statistic, Source


def to_approve(modeladmin, request, queryset):
    queryset.update(is_approved=True)


to_approve.short_description = "одобрить пост"


# вывод имен в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'create', 'is_approved']
    actions = [to_approve]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['date', 'name', 'source']


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Place)
admin.site.register(Statistic)
admin.site.register(Source)

