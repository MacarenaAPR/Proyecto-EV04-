from django import forms
from django.utils import timezone


class PricingForm(forms.Form):
    product_name = forms.CharField(
        max_length=100,
        label='Nombre del producto',
        help_text='Nombre del producto para identificarlo en el resultado.',
        error_messages={'required': 'Por favor ingresa un nombre de producto.'},
        widget=forms.TextInput(attrs={
            'title': 'Escribe el nombre del producto, por ejemplo: camiseta o shampoo.',
            'placeholder': 'ej: Cable USB, Camiseta, etc.',
        }),
    )
    current_stock = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label='Stock actual',
        help_text='Cantidad de unidades disponibles hoy en inventario.',
        error_messages={'required': 'Por favor ingresa el stock actual.'},
        widget=forms.NumberInput(attrs={
            'title': 'Ingresa cuántas unidades tienes disponibles ahora.',
            'placeholder': '0',
        }),
    )
    start_date = forms.DateField(
        label='Fecha de inicio',
        help_text='Selecciona la fecha inicial del periodo de ventas.',
        error_messages={'required': 'Por favor selecciona una fecha de inicio.'},
        widget=forms.DateInput(attrs={'type': 'date', 'title': 'Elige la fecha de inicio del periodo.'}),
    )
    end_date = forms.DateField(
        label='Fecha de fin',
        help_text='Selecciona la fecha final del periodo de ventas.',
        error_messages={'required': 'Por favor selecciona una fecha de fin.'},
        widget=forms.DateInput(attrs={'type': 'date', 'title': 'Elige la fecha final del periodo.'}),
    )
    total_sales = forms.DecimalField(
        min_value=0,
        max_digits=10,
        decimal_places=2,
        label='Ventas totales en el periodo',
        help_text='Unidades vendidas en ese periodo.',
        error_messages={'required': 'Por favor ingresa las ventas totales.'},
        widget=forms.NumberInput(attrs={
            'title': 'Ingresa cuántas unidades se vendieron durante ese tiempo.',
            'placeholder': '0',
        }),
    )
    current_price = forms.DecimalField(
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        label='Precio actual',
        help_text='Precio que tiene el producto actualmente.',
        error_messages={'required': 'Por favor ingresa el precio actual.'},
        widget=forms.NumberInput(attrs={
            'title': 'Escribe el precio actual que pagaría el cliente.',
            'placeholder': '0.00',
        }),
    )
    target_margin = forms.DecimalField(
        min_value=0.01,
        max_value=0.99,
        max_digits=4,
        decimal_places=2,
        initial=0.20,
        label='Margen objetivo (%)',
        help_text='Meta de utilidad que quieres mantener, por ejemplo 20% = 0.20.',
        error_messages={'required': 'Por favor ingresa un margen objetivo.'},
        widget=forms.NumberInput(attrs={
            'title': 'Indica el porcentaje de ganancia que quieres lograr.',
            'placeholder': '0.20',
        }),
    )
