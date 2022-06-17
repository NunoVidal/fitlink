from django.shortcuts import render
from .models import *
from .forms import *
from bootstrap_modal_forms.generic import BSModalCreateView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages


# Create your views here.
import json
def index(request):
    return render(request,'index.html',{})

def signin(request):
    return render(request,'sign-in.html',{})

def signup(request):
    return render(request,'sign-up.html',{})

def profile(request):
    context = PlanoTreino.objects.all().filter(refPersonalTrainer=PersonalTrainer.objects.get(username="larrywheels"))
    return render(request,'profile.html',{"planos": context})

def notifications(request):
    return render(request,'notifications.html',{})

def vr(request):
    return render(request,'virtual-reality.html',{})

def billing(request):
    return render(request,'billing.html',{})

def tables(request):
    return render(request,'tables.html',{})

def dashboard(request):
    return render(request,'dashboard.html',{})

def rtl(request):
    return render(request,'rtl.html',{})

def marketplace(request):
    context = PlanoTreino.objects.all()
    return render(request,'marketplace.html',{"planos": context})

def planMaker(request):
    context = {
        'tiposPlano': TipoPlano.objects.all(),
        'subscritores': Cliente.objects.all().filter(id__in=Subscricao.objects.values_list("refCliente_id").filter(refPT=PersonalTrainer.objects.get(username="larrywheels")))
    }
    print(context['subscritores'])
    return render(request,'planMaker.html',{'defaults': context})


class ExerciseAdder(View):
    template_name = 'addExercicioModal.html'
    def get(self, request):
        exercicios = Exercicio.objects.all()
        for ex in exercicios:
            ex.selected = False
        context_data = {'Exercicios': exercicios}
        return render(request,self.template_name,context_data)
   


class PlanAdder(View):
    def post(self, request):
        data = request.POST
        if(data['titulo'] == '' and data['tipoPlano'] == 1):
            messages.add_message(request, messages.ERROR, 'Titulo invalido')
            return HttpResponseRedirect("planMaker")

        if(data['descricao'] == '' and data['tipoPlano'] == 1):
            messages.add_message(request, messages.ERROR, 'Descricao invalido')
            return HttpResponseRedirect("planMaker")
            
        if((data['preco'] == '' or float(data['preco']) < 0) and data['tipoPlano'] == 1):
            messages.add_message(request, messages.ERROR, 'Preco invalido')
            return HttpResponseRedirect("planMaker")
            
        if('clientes' in data):
            if(len(data['clientes']) <=0 and data['tipoPlano'] == 2):
                messages.add_message(request, messages.ERROR, 'Selecione clientes')
                return HttpResponseRedirect("planMaker")
               
        if(int(data['duracaoBloco']) <= 0):
            messages.add_message(request, messages.ERROR, 'Duracao do bloco invalido')
            return HttpResponseRedirect("planMaker")
            
        if(int(data['nrBlocos']) <= 0):
            messages.add_message(request, messages.ERROR, 'Nr de blocos invalido')
            return HttpResponseRedirect("planMaker")
          
        PlanoTreino.objects.create(
            titulo=data['titulo'],
            imagem='default',
            descricao=data['descricao'],
            requisitos=data['requisitos'],
            tipoPlano=TipoPlano.objects.filter(id=data['tipoPlano']).first(),
            preco=data['preco'],
            periodoBloco=data['duracaoBloco'],
            nrBlocos=data['nrBlocos'],
            refPersonalTrainer=PersonalTrainer.objects.filter(username='larrywheels').first()
        )
        
        messages.add_message(request, messages.INFO, 'Plano Criado')
        return HttpResponseRedirect("profile")



def detalhesPlano(request,idPlano):
    return render(request,'detalhesPlano.html',{'plano': PlanoTreino.objects.filter(id=idPlano).first()})
