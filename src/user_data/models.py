from django.db import models


class UserData(models.Model):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    saldo = models.FloatField(default=0.0)
    limite_maximo = models.FloatField(default=0.0)
    # limite_disponivel = models.FloatField(default=0.0)  (derivado)

    def __str__(self):
        return self.email
