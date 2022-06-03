from .models import Exercicio
from bootstrap_modal_forms.forms import BSModalModelForm

class ExercicioModelForm(BSModalModelForm):
    class Meta:
        model = Exercicio
        fields = ['titulo', 'descricao', 'img']