from rest_framework import serializers
from cartao import models

class CartaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cartao
        fields = [
            # 'email',
            'id',
            'apelido_cartao',
            'limite_credito'
        ]
