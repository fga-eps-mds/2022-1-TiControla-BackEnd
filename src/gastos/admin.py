from django.contrib import admin
from gastos import models

admin.site.register(models.GastoCredito)
admin.site.register(models.GastoDebito)
admin.site.register(models.GastoFixo)
