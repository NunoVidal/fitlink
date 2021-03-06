import email
from textwrap import indent
from urllib import request
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from bootstrap_modal_forms.generic import BSModalCreateView
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import login
from django.contrib import messages
from datetime import date
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


# Create your views here.
import json
def index(request):
        return render(request,'index.html',{})

def signin(request):
    return render(request,'sign-in.html',{})

def signup(request):
    return render(request,'sign-up.html',{})

@login_required(login_url='login/')
def profile(request):
    if request.user.groups.filter(name="Personal Trainer"):
        context = PlanoTreino.objects.all().filter(refPersonalTrainer=User.objects.get(id=request.user.id))
    else:
        context = PlanoTreino.objects.all().filter(id__in=Compra.objects.filter(refCliente=request.user.id).values("refPlano"))
    print(context)
    return render(request,'profile.html',{"planos": context})

@login_required(login_url='login/')
def notifications(request):
    return render(request,'notifications.html',{})

@login_required(login_url='login/')
def vr(request):
    return render(request,'virtual-reality.html',{})

@login_required(login_url='login/')
def billing(request):
    return render(request,'billing.html',{})

@login_required(login_url='login/')
def tables(request):
    return render(request,'tables.html',{})

@login_required(login_url='login/')
def dashboard(request):
    return render(request,'dashboard.html',{})

@login_required(login_url='login/')
def rtl(request):
    return render(request,'rtl.html',{})

@login_required(login_url='login/')
def marketplace(request):
    context = PlanoTreino.objects.all()
    return render(request,'marketplace.html',{"planos": context})

@login_required(login_url='login/')
def planMaker(request):
    context = {
        'tiposPlano': TipoPlano.objects.all(),
        'subscritores': User.objects.all().filter(id__in=Subscricao.objects.values_list("refCliente_id").filter(refPT=User.objects.get(id=request.user.id)))
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

        exercicios = []          
        for bloco in range(int(data['nrBlocos'])):
            numbloco = bloco + 1
            for duracao in range(int(data['duracaoBloco'])):
                nduracao  = duracao + 1
                key = str(numbloco)+str(nduracao)
                if(('id_exercicio'+key) not in data):
                    messages.add_message(request, messages.ERROR, 'coloque exercicios no plano por favor')
                    return HttpResponseRedirect("planMaker")
                for ex in data['id_exercicio'+key]:
                    if(data['sets'+str(ex)+key] == '' or data['reps'+str(ex)+key] == '' ):
                        messages.add_message(request, messages.ERROR, 'Preencha todas sets e reps')
                        return HttpResponseRedirect("planMaker")

                    exercicios.append({'exercicio' : ex, 'sets': data['sets'+str(ex)+key], 'reps': data['reps'+str(ex)+key],'bloco': numbloco,'duracao':nduracao})

        idPlano = PlanoTreino.objects.create(
            titulo=data['titulo'],
            imagem='default',
            descricao=data['descricao'],
            requisitos=data['requisitos'],
            tipoPlano=TipoPlano.objects.filter(id=data['tipoPlano']).first(),
            preco=data['preco'],
            periodoBloco=data['duracaoBloco'],
            nrBlocos=data['nrBlocos'],
            refPersonalTrainer=User.objects.filter(id=request.user.id).first()
        )
        
        for reg in exercicios:
            ExercicioPlano.objects.create(
                refPlano=PlanoTreino.objects.latest('id'),
                refExercicio=Exercicio.objects.filter(id=reg['exercicio']).first(),
                nrBloco=reg['bloco'],
                periodoBloco=reg['duracao'],
                reps=reg['reps'],
                sets=reg['sets']
            ) 

        
        messages.add_message(request, messages.INFO, 'Plano Criado')
        return HttpResponseRedirect("profile")



@login_required(login_url='login/')
def detalhesPlano(request,idPlano):
    return render(request,'detalhesPlano.html',{'plano': PlanoTreino.objects.filter(id=idPlano).first()})

@login_required(login_url='login/')
def comprasSubscricao(request,idPlano):
    return render(request,'comprasSubscricao.html',{'plano': PlanoTreino.objects.filter(id=idPlano).first()})

class BuyPlan(View):
    def post(self, request):
        data = request.POST

        if(data['cardNumber'] == '' and data["pagamento"] == "credito"):
            messages.add_message(request, messages.ERROR, 'N??mero do Cart??o Invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])

        if(data['nome'] == '' and data["pagamento"] == "credito"):
            messages.add_message(request, messages.ERROR, 'Nome do Titular Invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])
        
        if(data['apelido'] == '' and data["pagamento"] == "credito"):
            messages.add_message(request, messages.ERROR, 'Apelido Invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])

        if((data['mes'] == '' or int(data['mes']) < 0 or int(data['mes']) > 12 ) and data["pagamento"] == "credito"):
            messages.add_message(request, messages.ERROR, 'Mes invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])

        if((data['Ano'] == '' or int(data['Ano']) < 0) and data["pagamento"] == "credito"):
            messages.add_message(request, messages.ERROR, 'Ano invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])
        
        if((data['CVV'] == '' or int(data['CVV']) < 0) and data["pagamento"] == "credito"):
            messages.add_message(request, messages.ERROR, 'CVV invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])
        
        if((data['email'] == '') and data["pagamento"] == "payP"):
            messages.add_message(request, messages.ERROR, 'Email invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])
        
        if((data['phone'] == '' or int(data['phone']) < 0) and data["pagamento"] == "MBway"):
            messages.add_message(request, messages.ERROR, 'N??mero do Telem??vel invalido')
            return HttpResponseRedirect("/comprasSubscricao/"+data['idPlano'])
        

        if data["pagamento"] == 'credito':
            dataC = date( int(data['Ano']),int(data['mes']),1)
            cvvC = data['CVV']
            cartao = data['cardNumber']
        else:
            dataC =  date(1970,1,1)
            cvvC = 0
            cartao = 0

        idpagamento = Pagamento.objects.create(
            nome=data['nome'],
            apelido=data['apelido'], 
            montante= data['montante'] , 
            emailPaypal=data['email'],
            entidade = 0, 
            referenciaMB=0, 
            nrCartao=cartao,
            cvv=cvvC,
            expireDate=dataC
        )

        idcompra = Compra.objects.create(
            dataCompra = date.today(),
            refPlano = PlanoTreino.objects.filter(id=data['idPlano']).first(),
            refCliente = User.objects.filter(id=request.user.id).first(), #login user
        )
       
        messages.add_message(request, messages.INFO, 'Pagamento efetuado')
        return HttpResponseRedirect("/marketplace")

        



@login_required(login_url='login/')
def exerciciosPlano(request,idPlano):

    exercicios = ExercicioPlano.objects.filter(refPlano=idPlano).all()
    contextExercicio = {}
    for ex in exercicios:
        if(ex.nrBloco not in contextExercicio):
            contextExercicio[ex.nrBloco] = {}
        
        if(ex.periodoBloco not in contextExercicio[ex.nrBloco]):
                contextExercicio[ex.nrBloco][ex.periodoBloco] = []
            
        contextExercicio[ex.nrBloco][ex.periodoBloco].append({'exercicio': Exercicio.objects.filter(id=ex.refExercicio.id).first(),'reps': ex.reps, 'sets': ex.sets})
        
    return render(request,'exerciciosPlano.html',{'plano': PlanoTreino.objects.filter(id=idPlano).first(),'exercicios': contextExercicio })


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data['usermode'] == True:
                group = Group.objects.get(name= "Personal Trainer")
                group.user_set.add(user)
            else:
                group = Group.objects.get(name= "Cliente")
                group.user_set.add(user)
            login(request, user)
            messages.success(request, "Acoount registration successful.")
            return redirect("profile")
        messages.error(request ,"Unsuccessfull registration. Invalid information")
    else:
        form = NewUserForm()
    return render (request=request, template_name="register.html",context={"register_form":form})