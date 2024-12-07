from django.db import models

class Website(models.Model):
    
    name = models.CharField(max_length=255)
    url = models.URLField()

    status = models.CharField(max_length=50, default='Pending') 
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url

