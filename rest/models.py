# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.gis.db import models


# Create your models here.
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


class Casino(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=200)
    location=models.PointField(null=True,blank=True ) # for storing the geographic points
    created_at=models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

#This is a signal that is fired or triggered immediately after a save is done on the AUTH_USER_MODELS
# This ensures every new user is generated for a token
@receiver(post_save,sender=settings.AUTH_USER_MODEL)

def create_auth_token(sender,instance=None,created=False,**kwargs):
    if created:
        Token.objects.create(user=instance)# If user was created, create token