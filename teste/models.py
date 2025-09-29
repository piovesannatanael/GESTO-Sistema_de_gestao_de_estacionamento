# teste/models.py
from django.db import models

class Teste(models.Model):
    nome = models.CharField(max_length=10)