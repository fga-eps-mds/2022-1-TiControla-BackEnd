from django.db import models
# from user_data import models as user_data_models

class Cartao(models.Model):

    email = models.EmailField(max_length=255, default="")
    limite_credito = models.FloatField(default=0.0)
    apelido_cartao = models.CharField(
        max_length=150, unique=True
    )

    # def __str__(self):
    #     return '%s: %s' % (self.email, self.apelido_cartao)
