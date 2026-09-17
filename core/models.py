from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    nota = models.IntegerField()

    comentario = models.TextField()

    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de {self.usuario.username}"