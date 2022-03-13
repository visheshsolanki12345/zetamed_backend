from django.db import models

# Create your models here.

class City(models.Model):
    city = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return str(self.city)

class State(models.Model):
    city = models.ManyToManyField(City)
    state = models.CharField(max_length=500, null=True, blank=True)
    def get_city(self):
        return ",".join([str(p) for p in self.city.all()])

    def __str__(self):
        return str(f"{self.state}")


class Country(models.Model):
    state = models.ManyToManyField(State)
    country = models.CharField(max_length=500, null=True, blank=True)

    def get_state(self):
        return ",".join([str(p) for p in self.state.all()])

    def __str__(self):
        return str(self.country)
    