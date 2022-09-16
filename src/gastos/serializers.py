from rest_framework import serializers
from gastos.models import GastoCredito, GastoDebito, GastoFixo
from django.db import models



class GastoCreditoSerializer(serializers.ModelSerializer):
   class Meta:
       model = GastoCredito
       fields = [
           'quantidade_parcelas',
           'date',
           'tipo',
           'nome',
           'descricao',
           'valor',
       ]


class GastoDebitoSerializer(serializers.ModelSerializer):
   class Meta:
       model = GastoDebito
       fields = [
           'date',
           'tipo',
           'nome',
           'descricao',
           'valor',
       ]


# o GastoDebito e o GastoFixo estão iguais por enquanto, mas é melhor deixar desacoplado
class GastoFixoSerializer(serializers.ModelSerializer):
   class Meta:
       model = GastoFixo
       fields = [
           'date',
           'tipo',
           'nome',
           'descricao',
           'valor',
       ]


# class GastoSerializer(serializers.ModelSerializer):

#         #    'user_data',
#     date = models.DateField()
#     tipo = models.CharField(max_length=50)
#     nome = models.CharField(max_length=50)
#     descricao = models.CharField(max_length=150)
#     valor = models.FloatField()
