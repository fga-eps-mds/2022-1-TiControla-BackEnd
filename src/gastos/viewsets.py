from gastos import serializers, models
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user


# TODO: deduplicate boilerplate code
class GastoCreditoView(generics.CreateAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GastoCreditoSerializer

    def post(self, request):
        # adiciona gasto_credito a lista de gastos do usuario
        kwargs = {
            'email': request.user.email,
            'id_cartao': request.data['id_cartao'],
            'date': request.data['date'],
        }

        for key in request.data.keys():
            if key == ['email', 'id']:
                continue
            kwargs[key] = request.data[key]

        # set default values for keys that are not in request.data
        for key in GastoCredito._meta.get_fields():
            if key.name not in kwargs.keys():
                kwargs[key.name] = key.get_default()

        gasto_credito = GastoCredito.objects.create(**kwargs)

        return Response(self.serializer_class(gasto_credito).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # lista todos os gastos credito do usuario
        try:
            gasto_credito_list = GastoCredito.objects.filter(email=request.user.email)
            return Response(self.serializer_class(gasto_credito_list, many=True).data, status=status.HTTP_200_OK)
        except GastoCredito.DoesNotExist:
            raise Http404('Not found')

    def patch(self, request):
        # altera gasto_credito da lista de gasto_credito do usuario por id
        gasto_credito = GastoCredito.objects.get(
            email=request.user.email,
            id=request.data['id']
        )
        
        for key in request.data.keys():
            if key in ['id', 'email']:
                continue
            setattr(gasto_credito, key, request.data[key])

        gasto_credito.save()
        return Response(self.serializer_class(gasto_credito).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        # deleta gasto_credito da lista de cartoes do usuario por id
        gasto_credito = GastoCredito.objects.get(
            email=request.user.email,
            id=request.data['id']
        )
        gasto_credito.delete()
        return Response(self.serializer_class(gasto_credito).data, status=status.HTTP_204_NO_CONTENT)



class GastoDebitoView(generics.CreateAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GastoDebitoSerializer

    def post(self, request):
        # adiciona gasto_debito a lista de gastos do usuario
        kwargs = {
            'email': request.user.email,
            'date': request.data['date'],
        }

        for key in request.data.keys():
            if key == ['email', 'id']:
                continue
            kwargs[key] = request.data[key]

        # set default values for keys that are not in request.data
        for key in GastoDebito._meta.get_fields():
            if key.name not in kwargs.keys():
                kwargs[key.name] = key.get_default()

        gasto_debito = GastoDebito.objects.create(**kwargs)

        return Response(self.serializer_class(gasto_debito).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # lista todos os gastos debito do usuario
        try:
            gasto_debito_list = GastoDebito.objects.filter(email=request.user.email)
            return Response(self.serializer_class(gasto_debito_list, many=True).data, status=status.HTTP_200_OK)
        except GastoDebito.DoesNotExist:
            raise Http404('Not found')

    def patch(self, request):
        # altera gasto_debito da lista de gasto_debito do usuario por id
        gasto_debito = GastoDebito.objects.get(
            email=request.user.email,
            id=request.data['id']
        )
        
        for key in request.data.keys():
            if key in ['id', 'email']:
                continue
            setattr(gasto_debito, key, request.data[key])

        gasto_debito.save()
        return Response(self.serializer_class(gasto_debito).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        # deleta gasto_debito da lista de cartoes do usuario por id
        gasto_debito = GastoDebito.objects.get(
            email=request.user.email,
            id=request.data['id']
        )
        gasto_debito.delete()
        return Response(self.serializer_class(gasto_debito).data, status=status.HTTP_204_NO_CONTENT)


class GastoFixoView(generics.CreateAPIView, generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.GastoFixoSerializer

    def post(self, request):
        # adiciona gasto_fixo a lista de gastos do usuario
        kwargs = {
            'email': request.user.email,
            'date': request.data['date'],
        }

        for key in request.data.keys():
            if key == ['email', 'id']:
                continue
            kwargs[key] = request.data[key]

        # set default values for keys that are not in request.data
        for key in GastoFixo._meta.get_fields():
            if key.name not in kwargs.keys():
                kwargs[key.name] = key.get_default()

        gasto_fixo = GastoFixo.objects.create(**kwargs)

        return Response(self.serializer_class(gasto_fixo).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        # lista todos os gastos fixo do usuario
        try:
            gasto_fixo_list = GastoFixo.objects.filter(email=request.user.email)
            return Response(self.serializer_class(gasto_fixo_list, many=True).data, status=status.HTTP_200_OK)
        except GastoFixo.DoesNotExist:
            raise Http404('Not found')

    def patch(self, request):
        # altera gasto_fixo da lista de gasto_fixo do usuario por id
        gasto_fixo = GastoFixo.objects.get(
            email=request.user.email,
            id=request.data['id']
        )
        
        for key in request.data.keys():
            if key in ['id', 'email']:
                continue
            setattr(gasto_fixo, key, request.data[key])

        gasto_fixo.save()
        return Response(self.serializer_class(gasto_fixo).data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        # deleta gasto_fixo da lista de cartoes do usuario por id
        gasto_fixo = GastoFixo.objects.get(
            email=request.user.email,
            id=request.data['id']
        )
        gasto_fixo.delete()
        return Response(self.serializer_class(gasto_fixo).data, status=status.HTTP_204_NO_CONTENT)

