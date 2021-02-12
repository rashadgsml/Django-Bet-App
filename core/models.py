import string
import random

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField()

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class BetSlip(models.Model):
    slug = models.SlugField(default='')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    games = models.ManyToManyField('Game')
    bet_slip_code = models.CharField(max_length=21, default='')
    accepted = models.BooleanField(default=False)
    status = models.CharField(max_length=10, default='NR')
    stake = models.FloatField(blank=True,null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.profile.user.username

    def get_overal_odd(self):
        overal_odd = 1
        for i in self.games.all():
            overal_odd = i.odd * overal_odd
        return overal_odd

    def get_potential_return(self):
        potential_return = float(self.get_overal_odd() * self.stake)
        return potential_return

    def save(self, *args, **kwargs):
        self.bet_slip_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
        value = self.bet_slip_code
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
    

class Game(models.Model):
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    location = models.CharField(max_length=50, blank=True)
    prediction = models.CharField(max_length=10, null=True)
    odd = models.FloatField(null=True)
    result = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=10, default='NR')

    def __str__(self):
        return f"{self.home_team}-{self.away_team}-{self.prediction}-{self.odd}-{self.status}"




