from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Saving(models.Model):
    member_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field="username", related_name="+",null=True, blank=True)  # User model field {foreign key}
    member_name = models.CharField(null=True, max_length=100)
    account_number = models.CharField(null=True, max_length=100)
    amount = models.CharField(null=True, max_length=100)
    date_of_payment = models.DateTimeField(null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    def __str__(self):
        return self.member_id
        
