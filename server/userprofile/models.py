from django.db import models
from django.contrib.auth.models import User
from userauth.models import CustomUser

# TODO: Add Image

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

# Create your models here.
class UserProfile(models.Model):
    occupation = models.CharField(max_length=100)
    residence = models.CharField(max_length=100)
    gender = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    nin = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self) -> str:
        return f"{self.occupation}"