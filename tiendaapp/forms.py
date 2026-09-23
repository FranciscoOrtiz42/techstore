from django import forms

from .models import Producto


# Formulario usado tanto para crear como para editar productos.
class ProductoForm(forms.ModelForm):
    # Estos límites se validan en el servidor y también se reflejan en el navegador.
    nombre = forms.CharField(
        label='Nombre',
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ej: Teclado mecánico RGB',
                'maxlength': 30,
            }
        ),
    )
    precio = forms.IntegerField(
        label='Precio (CLP)',
        min_value=0,
        widget=forms.NumberInput(attrs={'step': '1', 'min': '0', 'inputmode': 'numeric'}),
    )
    stock = forms.IntegerField(
        label='Stock',
        min_value=0,
        max_value=9999,
        widget=forms.NumberInput(
            attrs={'step': '1', 'min': '0', 'max': '9999', 'inputmode': 'numeric'}
        ),
    )
    descripcion = forms.CharField(
        label='Descripción',
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'maxlength': 300}),
    )

    class Meta:
        model = Producto
        # Se muestran en este orden para que coincida con el formulario de la aplicación.
        fields = ['nombre', 'categoria', 'precio', 'stock', 'descripcion']
        widgets = {
            'categoria': forms.TextInput(attrs={'placeholder': 'Ej: Periféricos'}),
        }