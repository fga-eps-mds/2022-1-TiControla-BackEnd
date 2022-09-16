from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user

from cartao import serializers
from cartao.models import Cartao
from gastos.models import GastoCredito

# O cartao pode ser visualizado pela profile view do usuario. Esta view server para criar, editar e deletar cartoes.
class CartaoView(generics.CreateAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.CartaoSerializer

    def post(self, request):
        # adiciona cartao a lista de cartoes do usuario
        kwargs = {
            'email': request.user.email,
            'apelido_cartao': request.data['apelido_cartao'],
        }

        for key in request.data.keys():
            if key in ['email', 'id']:
                continue
            print(key)
            kwargs[key] = request.data[key]

        print('continueee key')

        # set default values for keys that are not in request.data
        for key in Cartao._meta.get_fields():
            print(key)
            if key.name not in kwargs.keys():
                kwargs[key.name] = key.get_default()

        cartao = Cartao.objects.create(**kwargs)

        return Response(self.serializer_class(cartao).data, status=status.HTTP_201_CREATED)



    def get(self, request):
        # lista todos os cartoes do usuario
        try:
            cartao_list = Cartao.objects.filter(email=request.user.email)
            return Response(self.serializer_class(cartao_list, many=True).data, status=status.HTTP_200_OK)
        except Cartao.DoesNotExist:
            raise Http404('Not found')

    def patch(self, request):
        # altera cartao da lista de cartoes do usuario por id
        cartao = Cartao.objects.get(email=request.user.email, id=request.data['id'])

        for key in request.data.keys():
            if key in ['id', 'email']:
                continue
            setattr(cartao, key, request.data[key])

        cartao.save()
        return Response(self.serializer_class(cartao).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        # se houver algum gasto com esse cartao, nao pode deletar sem deletar o gasto antes
        if GastoCredito.objects.filter(id_cartao=request.data['id']).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        # deleta cartao da lista de cartoes do usuario por id
        cartao = Cartao.objects.get(email=request.user.email, id=request.data['id'])
        cartao.delete()
        return Response(self.serializer_class(cartao).data, status=status.HTTP_204_NO_CONTENT)
