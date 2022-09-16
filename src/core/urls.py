"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib.auth.views import password_reset
from django.contrib import admin

from django.urls import path, include
from rest_framework import routers
# from user.viewsets import UserViewSet
from user import viewsets as user_viewsets
from user_data import viewsets as user_data_viewsets
from cartao import viewsets as cartao_viewsets
from gastos import viewsets as gastos_viewsets


# route = routers.DefaultRouter()

# route.register(r'user', UserViewSet, basename="user")

urlpatterns = [
    path('admin/',
         admin.site.urls),
    path('register/',
         user_viewsets.RegisterView.as_view()),
    path('verification/',
         user_viewsets.VerifyAccountView.as_view(),name='verification'),
    path('login/',
         user_viewsets.LoginView.as_view()),
    path('logout/',
         user_viewsets.LogoutView.as_view()),
    path('profile/',
         user_viewsets.ProfileView.as_view()),
    # path('password-reset/',
        #  password_reset,name='password_reset'
    #),
    # retorna tambem os cartoes e gastos do usuario
    path('profile/data/',
         user_data_viewsets.UserDataView.as_view()),
    path('profile/limite-disponivel/mensal/',
         user_data_viewsets.LimiteDisponivelMensalView.as_view()),
    path('profile/saldo-disponivel/mensal/',
         user_data_viewsets.SaldoDisponivelMensalView.as_view()),
    path('profile/cartao/',
         cartao_viewsets.CartaoView.as_view()),
    path('profile/cartao/total/mensal/',
         user_data_viewsets.TotalPorCartaoPorMesView.as_view()),
    path('profile/gastos/debito/',
         gastos_viewsets.GastoDebitoView.as_view()),
    path('profile/gastos/debito/diario/',
         user_data_viewsets.GastoDebitoDiarioView.as_view()),
    path('profile/gastos/credito/',
         gastos_viewsets.GastoCreditoView.as_view()),
    path('profile/gastos/credito/diario/',
         user_data_viewsets.GastoCreditoDiarioView.as_view()),
    path('profile/gastos/fixo/',
         gastos_viewsets.GastoFixoView.as_view()),
]
