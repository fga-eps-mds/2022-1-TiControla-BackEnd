from django.db import models
from user_data import models as user_data_models
from cartao import models as cartao_models


class GastoCredito(models.Model):
    # user_data = models.ForeignKey(
    #     user_data_models.UserData,
    #     related_name="gasto_credito_list",
    #     on_delete=models.CASCADE
    # )

    # cartao = models.ForeignKey(
    #     cartao_models.Cartao,
    #     related_name="gasto_credito_list",
    #     on_delete=models.CASCADE
    # )
    
    email = models.EmailField(max_length=255, default="")
    id_cartao = models.BigIntegerField(serialize=False)

    quantidade_parcelas = models.FloatField(default=1)

    date = models.DateField(blank=False, auto_now_add=False)
    # exemplo: mercado, pessoal, lazer, carro...
    tipo = models.CharField(max_length=50, default="outros")
    nome = models.CharField(max_length=50, default="")
    descricao = models.CharField(max_length=150, default="")
    valor = models.FloatField(default=0.0)  # tem default, mas é obrigatorio


class GastoDebito(models.Model):
    email = models.EmailField(max_length=255, default="")

    date = models.DateField(blank=False, auto_now_add=False)
    # exemplo: mercado, pessoal, lazer, carro...
    tipo = models.CharField(max_length=50, default="outros")
    nome = models.CharField(max_length=50, default="")
    descricao = models.CharField(max_length=150, default="")
    valor = models.FloatField(default=0.0)  # tem default, mas é obrigatorio


# o GastoDebito e o GastoFixo estão iguais por enquanto, mas é melhor deixar desacoplado
class GastoFixo(models.Model):
    email = models.EmailField(max_length=255, default="")

    # misturar gasto fixo com quantidade de parcelas eh muito confuso
    # quantidade_parcelas = models.FloatField(default=1)

    # dia do mes em que cai o gasto fixo
    date = models.DateField(blank=False, auto_now_add=False)

    # exemplo: mercado, pessoal, lazer, carro...
    tipo = models.CharField(max_length=50, default="outros")
    nome = models.CharField(max_length=50, default="")
    descricao = models.CharField(max_length=150, default="")
    valor = models.FloatField(default=0.0)  # tem default, mas é obrigatorio
