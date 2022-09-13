from django.db import models
#from django.contrib.auth.models import User_data

class Cartao(models.Model):
    email = models.CharField(max_length=150, unique=True, primary_key=True) #id ou email (primary key do user_data)
    codigo = models.IntegerField(default=0.0)
    tipo = models.CharField(max_length=150) #credito ou debito 
    apelido_cartao = models.CharField(max_length=150)
    data = models.DateField (max_length=150)
    categoria = models.CharField (max_length=150)  #exemplo: mercado, pessoal, lazer, carro...
    descricao = models.CharField(max_length=150)
    valor = models.FloatField(default=0.0)

