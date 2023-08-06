from django.db import models
from django.contrib.auth.models import User

# just a shim, in production we will use the real Profile class in the actual otreehub repo.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def can_create_studio_project(self):
        return True
