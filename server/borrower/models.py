from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Borrower(models.Model):
    name = models.CharField(max_length=255)
    membership_id = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
