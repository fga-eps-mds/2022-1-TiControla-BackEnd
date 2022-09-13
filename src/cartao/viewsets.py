from cartao import serializers
from cartao import models
from rest_framework import generics, status, permissions, views, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user


# classe para mostrar/atualizar os dados do usuario, requer que o usuario esteja autenticado

class CartaoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CartaoSerializer
    queryset = models.Cartao.objects.all()