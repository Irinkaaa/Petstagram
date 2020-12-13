from django.db import models
from Petstagram.accounts.models import UserProfile
from Petstagram.pets.models import Pet


class Comment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
