from django.shortcuts import render
from .models import *
from .forms import *
from bootstrap_modal_forms.generic import BSModalCreateView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
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
            return HttpResponse(content=b'Preencha o Titulo pf', content_type=None, status=406, reason=None, charset=None, headers=None)

        if(data['descricao'] == '' and data['tipoPlano'] == 1):
            return HttpResponse(content=b'Preencha a descricao pf', content_type=None, status=406, reason=None, charset=None, headers=None)

        if((data['preco'] == '' or float(data['preco']) < 0) and data['tipoPlano'] == 1):
            return HttpResponse(content=b'Preco invalido', content_type=None, status=406, reason=None, charset=None, headers=None)

        if('clientes' in data):
            if(len(data['clientes']) <=0 and data['tipoPlano'] == 2):
                return HttpResponse(content=b'Selecione clientes', content_type=None, status=406, reason=None, charset=None, headers=None)

        if(int(data['duracaoBloco']) <= 0):
             return HttpResponse(content=b'Duracao do bloco invalida', content_type=None, status=406, reason=None, charset=None, headers=None)

        if(int(data['nrBlocos']) <= 0):
             return HttpResponse(content=b'Num de Blocos invalido', content_type=None, status=406, reason=None, charset=None, headers=None)

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

        return HttpResponse(content=b'Sucesso', content_type=None, status=200, reason=None, charset=None, headers=None)



def detalhesPlano(request):
    return render(request,'detalhesPlano.html',{})