#coding=utf-8

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Participante(models.Model):
        user = models.OneToOneField(User)
        ativo = models.BooleanField(default=True)


# definition of UserProfile from above
# ...

def criar_registro_participante(sender, instance, created, **kwargs):
    if created:
        Participante.objects.create(user=instance)

post_save.connect(criar_registro_participante, sender=User)        
        