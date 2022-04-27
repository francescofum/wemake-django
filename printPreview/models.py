from django.db import models

# Create your models here.

class STL(models.Model):

    url = models.URLField(max_length=500)
    file = models.FileField(upload_to='STL')
    pretty_name = models.CharField(max_length=255)
    upload_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pretty_name
