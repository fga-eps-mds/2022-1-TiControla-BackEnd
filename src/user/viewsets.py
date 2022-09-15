from django.contrib.auth import login, logout, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from user import serializers, tokens, models

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        sessionid = request.session.session_key
        csrftoken = request.session._session_cache['_auth_user_hash']
        response_content = {
            'sessionid': sessionid,
            'csrftoken': csrftoken,
        }
        return Response(response_content, status=status.HTTP_200_OK)


class LogoutView(views.APIView):

    def post(self, request, format=None):
        logout(request)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# classe para mostrar/atualizar os dados do usuario, requer que o usuario esteja autenticado
class ProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = serializers.UserSerializer

    def get_object(self):
        # returns the data that belongs to the user
        return self.request.user

    def patch_object(self):
        # atualiza somente o nome do usuario
        self.request.user.patch(full_name=self.request.data.full_name)
        return Response(None, status=status.HTTP_202_ACCEPTED)


class RegisterView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        user_model = get_user_model()
        current_user = user_model.objects.create_user(**request.data)
        
        # generate link to verify the user email
        verify_token = tokens.default_token_generator.make_token(current_user)
        # get the current url of the server
        current_domain = get_current_site(request).domain
        relative_link = reverse('verification')

        link = current_domain + relative_link + '?email=' + current_user.email + '&token=' + verify_token
        # check if the server is using http or https
        if request.is_secure():
            link = 'https://' + link
        else:
            link = 'http://' + link
        # send email with link to verify the user email
        current_user.email_user(
            subject='Ative sua conta do TiControla.',
            message='Acesse o seguinte link para validar a sua conta:\n' + link
        )
        return Response(None, status=status.HTTP_202_ACCEPTED)


class VerifyAccountView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        token = request.GET.get('token')

        # get user from the request email
        current_user = models.User.objects.get(email=request.GET.get('email'))

        if not current_user:
            return Response(None, status=status.HTTP_404_NO_CONTENT)

        if not tokens.default_token_generator.check_token(current_user, token):
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        current_user.is_verified = True
        current_user.save()

        return Response(None, status=status.HTTP_202_ACCEPTED)
