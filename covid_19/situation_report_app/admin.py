from django.contrib import admin
from .models import Article, Place, Post, Statistic, Source


# Register your models here.
admin.site.register(Post)
admin.site.register(Article)
admin.site.register(Place)
admin.site.register(Statistic)
admin.site.register(Source)

