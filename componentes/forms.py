from .models import (Componentes, Actividades, LONGUITUD_MAXIMA,
                     FORMATO_CARACTER_INCORRECTO, FORMATO_NUMERO_INCORRECTO,
                     VALOR_MAXIMO, VALOR_MINIMO, VALOR_MAXIMO_CAN,
                     LONGUITUD_MAXIMA_SALDO)
from django.forms import ModelForm, TextInput, Select, NumberInput


class ComponenteForm(ModelForm):
    class Meta:
        model = Componentes
        exclude = ['activo']

        widgets = {
            'nombre_componente': TextInput(attrs={'class': 'input-form form-control'}),
        }

        error_messages = {
            'nombre_componente': {'max_length': LONGUITUD_MAXIMA,
                                'required': 'Campo requerido',
                                'invalid': FORMATO_CARACTER_INCORRECTO
                                },
        }

    '''def save(self, commit=True):
        actividades = super(ComponenteForm, self).save(commit=False)
        if commit:
            actividades.save()
        return actividades'''


class ActividadesForm(ModelForm):
    class Meta:
        model = Actividades
        exclude = ['componentes']

        widgets = {
            'nombre_actividad': TextInput(attrs={'class': 'form-control'}),
            'unidad_medida_presupuestal': TextInput(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
            'recurso disponible': NumberInput(attrs={'class': 'form-control'}),

        }
        error_messages = {
            'nombre_actividad': {
                'max_length': LONGUITUD_MAXIMA,
                'required': 'Requerido',
                'invalid': FORMATO_CARACTER_INCORRECTO
            },
            'unidad_medida_presupuestal': {
                'max_length': LONGUITUD_MAXIMA,
                'required': 'Requerido'
            },
            'cantidad': {
                'max_length': LONGUITUD_MAXIMA,
                'required': 'Requerido',
                'invalid': FORMATO_NUMERO_INCORRECTO,
                'invalid': VALOR_MAXIMO_CAN,
                'invalid': VALOR_MINIMO
            },
            'recurso_disponible': {
                'max_digits': LONGUITUD_MAXIMA_SALDO,
                'required': 'Requerido',
                'invalid': FORMATO_NUMERO_INCORRECTO,
                'invalid': VALOR_MAXIMO,
                'invalid': VALOR_MINIMO
            }
        }
