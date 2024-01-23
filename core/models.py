from django.db import models

class Senha(models.Model):
    titulo = models.CharField(max_length=64)
    descricao = models.CharField(max_length=128)
    usuario = models.CharField(max_length=128)
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.titulo