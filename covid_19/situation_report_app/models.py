from django.db import models


# abstract class
class Date(models.Model):
    date = models.DateField(null=True)

    class Meta:
        abstract = True


# Create your models here.
class Place(models.Model):
    place_name = models.CharField(max_length=16, unique=True)
    country = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.place_name


class Source(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Article(Date):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Statistic(Date):
    country_name = models.ForeignKey(Place, on_delete=models.CASCADE)
    total_cases = models.CharField(max_length=8, null=True)
    new_cases = models.CharField(max_length=8, null=True)
    total_deaths = models.CharField(max_length=8, null=True)
    new_deaths = models.CharField(max_length=8, null=True)
    total_recovered = models.CharField(max_length=8, null=True)

    # def __str__(self):
    #     return self.name


class Post(models.Model):
    name = models.CharField(max_length=32, unique=True)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts', null=True, blank=True)

    def __str__(self):
        return self.name
