from django.db import models

# Create your models here.
class House(models.Model):

    """Model Definition for House"""

    name = models.CharField(max_length=140)
    price_per_night = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=140)
    pet_allowed = models.BooleanField(default=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
