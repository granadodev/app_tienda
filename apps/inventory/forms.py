from django import forms
from .models import Products

class ProductosForm(forms.ModelForm):
    class Meta:
        #indicamos cual es el modelo del    que se creara este formulario
        model = Products
        fields = ['name','stock','unit_measurement','price_by']
        widgets = { #Esto es para acomodar el formulario a nuesrto gusto, como si lo hicieramos ene l html
            "name": forms.TextInput(attrs={'class':'form-control', 'placeholder':'Escriba el nombre del producto'}),
            "stock": forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Escriba el stock del producto'}),
            "unit_measurement": forms.Select(attrs={'class': 'form-select'}),
            "price_by": forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Escriba el precio'}),
        }