from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        # Indicamos cuál es el modelo del que se creará este formulario
        model = Customer
        fields = ['name', 'number_phone', 'mail', 'address', 'active']
        
        # Corregimos los widgets para que coincidan con los campos de arriba
        widgets = {
            "name": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escriba el nombre completo'}),
            
            "number_phone": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: +57 300 123 4567'}),
            
            "mail": forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            
            "address": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de residencia'}),
            
            # Para un campo booleano (True/False), usamos el switch/checkbox de Bootstrap
            "active": forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }