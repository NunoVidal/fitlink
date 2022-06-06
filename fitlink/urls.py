

from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
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
] 