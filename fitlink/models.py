from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class TipoPlano(models.Model):
    tipo = models.CharField(max_length = 255)
    def __str__(self):
        return self.tipo


class PlanoTreino(models.Model):
    titulo = models.CharField(max_length = 255)
    imagem = models.CharField(max_length=255)
    descricao = models.TextField()
    requisitos = models.TextField()
    tipoPlano = models.ForeignKey(TipoPlano, on_delete=models.CASCADE)
    preco = models.FloatField()
    periodoBloco = models.IntegerField()
    nrBlocos = models.IntegerField()
    refPersonalTrainer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Compra(models.Model):
    dataCompra = models.DateField(auto_now_add=True)
    refPlano = models.ForeignKey(PlanoTreino, on_delete=models.CASCADE)
    refCliente = models.ForeignKey(User,on_delete=models.CASCADE)

class Pagamento(models.Model):
    nome = models.CharField( max_length=255)
    apelido = models.CharField( max_length=255)
    montante = models.FloatField()
    emailPaypal = models.EmailField( max_length=254)
    entidade = models.IntegerField()
    referenciaMB = models.IntegerField()
    nrCartao = models.IntegerField()
    cvv = models.IntegerField()
    expireDate = models.DateField()



class Exercicio(models.Model):
    titulo = models.CharField(max_length = 255)
    img = models.CharField(max_length=255)
    descricao = models.TextField()


class ExercicioPlano(models.Model):
    refPlano = models.ForeignKey(PlanoTreino, on_delete=models.CASCADE)
    refExercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    nrBloco = models.IntegerField()
    periodoBloco = models.IntegerField()
    reps = models.IntegerField()
    sets = models.IntegerField()



class Subscricao(models.Model):
    refPT = models.ForeignKey(User, on_delete=models.CASCADE, related_name='personal_trainer')
    refCliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cliente')