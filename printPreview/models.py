from django.db import models

# Create your models here.




class STL(models.Model):

    url = models.URLField(max_length=500)
    file = models.FileField(upload_to='STL')
    pretty_name = models.CharField(max_length=255)
    upload_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pretty_name



class STL_TEMP(models.Model):
    """
    STL_TEMP represents stl files that are not products or 'to be printed' but are instead only uploaded to be sliced, and then can be safely deleted. 
    """


    url = models.URLField(max_length=500)
    file = models.FileField(upload_to='temp')
    pretty_name = models.CharField(max_length=255)
    upload_data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pretty_name