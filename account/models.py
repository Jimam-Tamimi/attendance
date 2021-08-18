from home.models import MyUser
from django.db import models

# Create your models here.
class ResetPassRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False, blank=False)
    new_pass = models.TextField('New Password', blank=False, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)