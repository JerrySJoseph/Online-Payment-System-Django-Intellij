from django.db import models
from django.contrib.auth.models import User


# Currency class used as an enum to denote allowed currencies
class Currency(models.TextChoices):
    GBP = 'GBP', 'British Pound'
    USD = 'USD', 'United States Dollar'
    EUR = 'EUR', 'Euro'


# Profile Model to hold user profile data
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    base_currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.USD)
    profile_pic = models.ImageField(upload_to='profile_images', blank=True, default='default.png')

    def __str__(self) -> str:
        return f'Profile [ {self.user.username} ]'
