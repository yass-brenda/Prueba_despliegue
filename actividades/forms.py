from .models import Actividad
from django.forms import ModelForm, TextInput, Select, NumberInput


class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        exclude = ['estatus']
        widgets = {
            'programa': Select(attrs={'class': 'input-form form-control',
                                      'style': 'width:250px'}),
            'nombre': TextInput(attrs={'class': 'input-form form-control',
                                       'style': 'width:250px'}),
            'presupuesto': NumberInput(attrs={'class': 'input-form form-control',
                                              'style': 'width:250px'}),
            'responsable': Select(attrs={'class': 'input-form form-control',
                                         'style': 'width:250px'}),
        }


class EdicionActividadForm(ModelForm):
    class Meta:
        model = Actividad
        fields = "__all__"
        widgets = {
            'programa': Select(attrs={'class': 'input-form form-control',
                                      'style': 'width:250px'}),
            'nombre': TextInput(attrs={'class': 'input-form form-control',
                                       'style': 'width:250px'}),
            'presupuesto': NumberInput(attrs={'class': 'input-form form-control',
                                              'style': 'width:250px'}),
            'responsable': Select(attrs={'class': 'input-form form-control',
                                         'style': 'width:250px'}),
            'estatus': Select(attrs={'class': 'input-form form-control',
                                     'style': 'width:250px'}),
        }
