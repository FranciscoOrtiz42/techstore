from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    precio = forms.IntegerField(
        label='Precio (CLP)',
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '1', 'min': '0', 'inputmode': 'numeric'}),
    )
    stock = forms.IntegerField(
        label='Stock',
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '1', 'min': '0', 'inputmode': 'numeric'}),
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Teclado mecánico RGB'}),
            'categoria': forms.TextInput(attrs={'placeholder': 'Ej: Periféricos'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }