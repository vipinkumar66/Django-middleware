from django.db import models

# Create your models here.
class NewStats(models.Model):
    win = models.IntegerField()
    mac = models.IntegerField()
    iph = models.IntegerField()
    android = models.IntegerField()
    oth = models.IntegerField()