from django.db import models


# Create your models here.
class Pet(models.Model):
    CAT = 'cat'
    DOG = 'dog'
    PARROT = 'parrot'
    PET_TYPES = [
        (CAT, 'Cat'),
        (DOG, 'Dog'),
        (PARROT, 'Parrot'),
    ]

    type = models.CharField(choices=PET_TYPES, max_length=6, blank=False)
    name = models.CharField(max_length=6, blank=False)
    age = models.PositiveIntegerField(blank=False)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='pets',)

    def __str__(self):
        return f'{self.id}: {self.name} who is a {self.type}'


class Like(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    field = models.CharField(max_length=2)
