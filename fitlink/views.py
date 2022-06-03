from django.shortcuts import render
from .models import *
from .forms import *
from bootstrap_modal_forms.generic import BSModalCreateView
from django.views import View
from django.urls import reverse_lazy
# Create your views here.

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
        'blocos':[
            {
                'nr': 1,
                'diaBloco':[{
                        'nr': 1,
                        'exercicios': []
                     },
                     {
                        'nr': 2,
                        'exercicios': []
                     },
                      {
                        'nr': 3,
                        'exercicios': []
                     }]
                
            },
             {
               'nr': 2,
             'diaBloco':[{
                    'nr': 1,
                    'exercicios': []
                    },
                    {
                    'nr': 2,
                    'exercicios': []
                    },
                    {
                    'nr': 3,
                    'exercicios': []
                    }]
             },
            
        ]
    }
    return render(request,'planMaker.html',{'defaults': context})


class ExerciseAdder(View):
    template_name = 'addExercicioModal.html'
    def get(self, request):
        exercicios = Exercicio.objects.all()
        for ex in exercicios:
            ex.selected = False
        context_data = {'Exercicios': exercicios}
        return render(request,self.template_name,context_data)
   
