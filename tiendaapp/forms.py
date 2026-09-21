from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Teclado mecánico RGB'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ej: Periféricos'}),
            'precio': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }