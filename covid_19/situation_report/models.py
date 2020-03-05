from django.db import models


# Create your models here.
class Place(models.Model):
    place_name = models.CharField(max_length=16, unique=True)
    country = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.place_name


class New(models.Model):
    name = models.CharField(max_length=32)
    url = models.CharField(max_length=64)
    date = models.DateField(null=True)

    def __str__(self):
        return self.name


class Statistic(models.Model):
    country_name = models.ForeignKey(Place, on_delete=models.CASCADE)
    date = models.DateField(null=True)
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

    def __str__(self):
        return self.name
