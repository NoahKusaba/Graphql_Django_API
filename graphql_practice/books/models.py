from django.db import models


# python manage.py makemigrations
# Create your models here.
class Books(models.Model):
    title = models.CharField(max_length=100)
    name = models.CharField(max_length= 50)
    excerpt = models.TextField()

    def __str__(self):
        return self.title


class Authors(models.Model):
    name = models.CharField(max_length=50)
    field = models.TextField()
