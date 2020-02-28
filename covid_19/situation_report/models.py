from django.db import models


# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=16, unique=True)
    country = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name


class New(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    create = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return self.name


class Statistic(models.Model):
    country = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateTimeField()
    total_cases = models.IntegerField()
    new_cases = models.IntegerField()
    total_deaths = models.IntegerField()
    new_deaths = models.IntegerField()
    total_recovered = models.IntegerField()

    def __str__(self):
        return self.country


class Post(models.Model):
    name = models.CharField(max_length=32, unique=True)
    text = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
