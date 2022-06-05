from django.contrib import admin
from .models import PersonalTrainer,Cliente,PlanoTreino,TipoPlano,Exercicio,Subscricao
# Register your models here.

admin.site.register(PersonalTrainer)
admin.site.register(Cliente)
admin.site.register(PlanoTreino)
admin.site.register(TipoPlano)
admin.site.register(Exercicio)
admin.site.register(Subscricao)