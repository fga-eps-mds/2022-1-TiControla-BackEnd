from django.db import models
from user import models as user_models

class Cartao(models.Model):
    user = models.ForeignKey(
        user_models.User,
        related_name="cartao_list",
        on_delete=models.CASCADE
    )

    codigo = models.IntegerField(default=0.0)

    # credito ou debito
    tipo = models.CharField(max_length=150)

    apelido_cartao = models.CharField(max_length=150, unique=True)

    data = models.DateField(max_length=150)

    # exemplo: mercado, pessoal, lazer, carro...
    categoria = models.CharField(max_length=150)

    descricao = models.CharField(max_length=150)

    valor = models.FloatField(default=0.0)

    class Meta:
        unique_together = ['user', 'apelido_cartao']
        # ordering = ['apelido_cartao']

    def __str__(self):
        return '%s: %s' % (self.user, self.apelido_cartao)
