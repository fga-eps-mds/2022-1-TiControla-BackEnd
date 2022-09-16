from rest_framework import serializers
from user_data import models
from cartao import models as cartao_models
from gastos import models as gastos_models


class UserDataSerializer(serializers.ModelSerializer):
    # cartao_list = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=False,
    #     queryset=cartao_models.Cartao.objects.all()
    # )
    # gasto_credito_list = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=False,
    #     queryset=gastos_models.GastoCredito.objects.all()
    # )
    # gasto_debito_list = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=False,
    #     queryset=gastos_models.GastoDebito.objects.all()
    # )
    # gasto_fixo_list = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=False,
    #     queryset=gastos_models.GastoFixo.objects.all()
    # )

    class Meta:
        model = models.UserData
        fields = [
            'email',
            'saldo',
            'limite_maximo',
            # 'cartao_list',
            # 'gasto_credito_list',
            # 'gasto_debito_list',
            # 'gasto_fixo_list',
            # 'limite_disponivel', (derivado)
        ]
