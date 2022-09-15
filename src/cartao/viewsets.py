from cartao import serializers
from cartao import models
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user


# classe para mostrar/atualizar os dados do usuario, requer que o usuario esteja autenticado

# class CartaoViewSet(generics.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = serializers.CartaoSerializer
#     queryset = models.Cartao.objects.all()
    

# class UserCartaoList(generics.ListAPIView):
#     queryset = models.Cartao.objects.all()
#     serializer_class = SubColectivoSerializer

#     def get_queryset(self):
#         cartao_id = self.kwargs["pk"]
#         return SubColectivo.objects.filter(colectivo=colectivo_id)

# classe para mostrar/atualizar os dados do usuario, requer que o usuario esteja autenticado
class UserCartaoListView(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CartaoSerializer

    # listar cartoes do usuario
    def get_object(self):
        # returns the data that belongs to the user
        return models.Cartao.objects.get(user=self.request.user)

    # criar um cartao para um usuario
    # 


# criar n cartaos
# alterar cartao i
# 
