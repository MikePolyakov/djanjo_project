from django.contrib import admin
from .models import New, Place, Post, Statistic


# Register your models here.
admin.site.register(Post)
admin.site.register(New)
admin.site.register(Place)
admin.site.register(Statistic)

