from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from django.contrib.auth import get_user

from user_data.models import UserData
from user_data.serializers import UserDataSerializer
from gastos.models import GastoCredito, GastoDebito, GastoFixo
from gastos.serializers import GastoCreditoSerializer, GastoDebitoSerializer, GastoFixoSerializer

# classe para mostrar/atualizar os dados do usuario, requer que o usuario esteja autenticado
class UserDataView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get_object(self):
        # returns the data that belongs to the user
        return UserData.objects.get(email=self.request.user.email)

    def patch_object(self):
        # updates the user's data
        UserData.objects.get(email=self.request.user.email).patch(**self.request.data)
        return Response(None, status=status.HTTP_202_ACCEPTED)


# mostra todos os limites disponiveis (cartao de credito) por mes para determinado usuario
class LimiteDisponivelMensalView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get(self, request, format=None):
        limite_disponivel_dict = {}
        user_data = UserData.objects.get(
            email=self.request.user.email
        )
        gasto_credito_list = GastoCredito.objects.filter(
            email=request.user.email
        )
        # limite maximo mensal do usuario
        limite_maximo = user_data.limite_maximo
        # calcular o gasto total por mes
        # TODO: lidar com anos tambem
        for gasto in gasto_credito_list:
            if gasto.date.month not in limite_disponivel_dict.keys():
                limite_disponivel_dict[gasto.date.month] = 0
            limite_disponivel_dict[gasto.date.month] += gasto.valor
        # subtrair gasto total mensal do limite maximo para achar o limite ainda disponivel para o mes
        for month in limite_disponivel_dict.keys():
            limite_disponivel_dict[month] = limite_maximo - \
                limite_disponivel_dict[month]
        # retornar o dicionario em formato json
        return Response(limite_disponivel_dict, status=status.HTTP_202_ACCEPTED)


# mostra todos os saldos disponiveis (debito e gastos fixos) por mes para determinado usuario
class SaldoDisponivelMensalView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get(self, request, format=None):
        saldo_disponivel_dict = {}
        user_data = UserData.objects.get(
            email=self.request.user.email
        )
        # saldo maximo mensal do usuario
        saldo_mensal = user_data.saldo
        # calcular o gasto total por mes
        gasto_debito_list = GastoDebito.objects.filter(
            email=request.user.email
        )
        gasto_fixo_list = GastoFixo.objects.filter(
            email=request.user.email
        )
        for gasto in [*gasto_debito_list, *gasto_fixo_list]:
            if gasto.date.month not in saldo_disponivel_dict.keys():
                saldo_disponivel_dict[gasto.date.month] = 0
            saldo_disponivel_dict[gasto.date.month] += gasto.valor
        # subtrair gasto total mensal do saldo mensal para achar o saldo ainda disponivel para o mes
        for month in saldo_disponivel_dict.keys():
            saldo_disponivel_dict[month] = saldo_mensal - \
                saldo_disponivel_dict[month]
        # retornar o dicionario em formato json
        return Response(saldo_disponivel_dict, status=status.HTTP_202_ACCEPTED)


# mostra todos os gastos (credito) por dia para determinado usuario
class GastoCreditoDiarioView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get(self, request, format=None):
        gastos_dict = {}
        user_data = UserData.objects.get(
            email=self.request.user.email
        )
        # TODO: levar em conta quantidade de parcelas
        # agrupar gastos por dia e por mes
        gasto_credito_list = GastoCredito.objects.filter(
            email=request.user.email
        )
        for gasto in gasto_credito_list:
            if gasto.date.month not in gastos_dict.keys():
                gastos_dict[gasto.date.month] = {}
            gastos_dict[gasto.date.month][gasto.date.day] = GastoCreditoSerializer(
                gasto
            ).data
        # retornar o dicionario em formato json
        return Response(gastos_dict, status=status.HTTP_202_ACCEPTED)


# mostra todos os gastos (debito e gastos fixos) por dia para determinado usuario
class GastoDebitoDiarioView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get(self, request, format=None):
        gastos_dict = {}
        user_data = UserData.objects.get(
            email=self.request.user.email
        )
        gasto_debito_list = GastoDebito.objects.filter(
            email=request.user.email
        )
        gasto_fixo_list = GastoFixo.objects.filter(
            email=request.user.email
        )
        # agrupar gastos por dia e por mes
        for gasto in [*gasto_debito_list, *gasto_fixo_list]:
            if gasto.date.month not in gastos_dict.keys():
                gastos_dict[gasto.date.month] = {}
            gastos_dict[gasto.date.month][gasto.date.day] = GastoDebitoSerializer(
                gasto
            ).data
        # retornar o dicionario em formato json
        return Response(gastos_dict, status=status.HTTP_202_ACCEPTED)


class TotalPorCartaoPorMesView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDataSerializer

    def get(self, request, format=None):
        total_por_cartao_dict = {}
        user_data = UserData.objects.get(
            email=self.request.user.email
        )
        gasto_credito_list = GastoCredito.objects.filter(
            email=request.user.email
        )
        # agrupar total de gastos credito por mes por cartao
        for gasto_credito in gasto_credito_list:
            if gasto_credito.id_cartao not in total_por_cartao_dict.keys():
                total_por_cartao_dict[gasto_credito.id_cartao] = 0
            total_por_cartao_dict[gasto_credito.id_cartao] += gasto_credito.valor
        # retornar o dicionario em formato json
        return Response(total_por_cartao_dict, status=status.HTTP_202_ACCEPTED)
