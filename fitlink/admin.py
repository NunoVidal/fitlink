from django.contrib import admin
from .models import PlanoTreino,TipoPlano,Exercicio,Subscricao,Compra
# Register your models here.


admin.site.register(PlanoTreino)
admin.site.register(TipoPlano)
admin.site.register(Exercicio)
admin.site.register(Subscricao)
admin.site.register(Compra)