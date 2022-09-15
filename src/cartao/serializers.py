from rest_framework import serializers
from cartao import models

class CartaoSerializer(serializers.ModelSerializer):

   class Meta:
       model = models.Cartao
       fields = [
           'user',
           'codigo',
           'tipo',
           'apelido_cartao',
           'data',
           'categoria',
           'descricao',
           'valor',
       ]
