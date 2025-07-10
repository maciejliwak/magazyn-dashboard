from django.contrib.auth.models import User
from django.db import models
from magazyn_core.models import Magazyn

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    magazyn = models.ForeignKey(Magazyn, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username} → {self.magazyn.nazwa if self.magazyn else 'brak'}"
