from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Loan(models.Model):
    member_name = models.CharField(max_length=100)
    member_id = models.ForeignKey(User, on_delete=models.CASCADE,to_field="username", blank=True, null=True, related_name="member") # membership_id of user model
    type = models.CharField(max_length=100)
    plan = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    granteers = models.CharField(max_length=100)
    remaining_amount = models.CharField(max_length=100, blank=True)
    reference_no = models.CharField(max_length=100, blank=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.member_name