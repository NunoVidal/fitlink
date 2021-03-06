

from django.urls import path,  include
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('',views.profile,name="index"),
    path('sign-in',views.signin,name="signin"),
    path('sign-up',views.signup,name="signup"),
    path('profile',views.profile,name="profile"),
    path('notifications',views.notifications,name="notifications"),
    path('virtual-reality',views.vr,name="virtual-reality"),
    path('billing',views.billing,name="billing"),
    path('tables',views.tables,name="tables"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('rtl',views.rtl,name="rtl"),
    path('marketplace',views.marketplace,name="marketplace"),
    path('planMaker',views.planMaker,name="planMaker"),
    path('addExercicio', views.ExerciseAdder.as_view(), name='addExercicio'),
    path('addPlano', views.PlanAdder.as_view(), name='addPlano'),
    path('comprasSubscricao/buyPlano', views.BuyPlan.as_view(), name='buyPlano'),
    path('detalhesPlano/<int:idPlano>', views.detalhesPlano, name='detalhesPlano'),
    path('exerciciosPlano/<int:idPlano>', views.exerciciosPlano, name='exerciciosPlano'),
    path('comprasSubscricao/<int:idPlano>', views.comprasSubscricao, name='comprasSubscricao'),
    path('register/', views.register_request, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'),name="login"),
    path('', include("django.contrib.auth.urls")),
] 