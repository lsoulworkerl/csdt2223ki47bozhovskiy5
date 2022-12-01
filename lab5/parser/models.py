from django.db import models
from django.urls import reverse

class Data(models.Model):
    input = models.IntegerField()
    output = models.IntegerField()

    class Meta:
        db_table = 'data'
    
    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.input})