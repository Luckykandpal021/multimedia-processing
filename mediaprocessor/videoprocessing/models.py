from django.db import models

# Create your models here.

class Books(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=150)
    date=models.DateField()
    time=models.TimeField()


class VideoProcess(models.Model):
    input_video=models.FileField(upload_to='videoes/')

