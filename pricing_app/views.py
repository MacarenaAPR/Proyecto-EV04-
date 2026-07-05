from datetime import date

from django.shortcuts import render

from .forms import PricingForm


def pricing_home(request):
    form = PricingForm()
    result = None

    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():
            stock = float(form.cleaned_data['current_stock'])
            sales = float(form.cleaned_data['total_sales'])
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            price = float(form.cleaned_data['current_price'])
            target_margin = float(form.cleaned_data['target_margin'])

            if end_date < start_date:
                form.add_error('end_date', 'La fecha de fin debe ser igual o posterior a la fecha de inicio.')
            else:
                days = (end_date - start_date).days + 1
                if days <= 0:
                    form.add_error('end_date', 'La fecha de fin debe ser posterior a la fecha de inicio.')
                else:
                    sales_rate = sales / days if days > 0 else 0
                    # --- MODELO MATEMÁTICO NORMALIZADO POR TIEMPO ---
                    # --- MODELO MATEMÁTICO SENSIBLE AL TIEMPO ---
                    p0 = price
                    sales_rate = sales / days if days > 0 else 0

                    # 1. Definimos una elasticidad base según el margen
                    elasticidad_base = 1.0 + (1.0 - target_margin)

                    # 2. INTRODUCIMOS EL FACTOR TEMPORAL: 
                    # Ajustamos la elasticidad según la velocidad de ventas.
                    # A mayor velocidad (sales_rate), menor sensibilidad al precio (elasticidad más baja -> precio más alto).
                    # A menor velocidad, mayor sensibilidad (elasticidad más alta -> precio más bajo).
                    factor_velocidad = 1 + (sales_rate * 0.2) # Ajuste: más ventas por día reduce la elasticidad
                    elasticidad_dinamica = elasticidad_base / factor_velocidad

                    # 3. Calculamos con la elasticidad dinámica
                    # q0 es la proyección a 30 días para mantener la escala
                    q0 = sales_rate * 30 
                    b = (q0 / p0) * elasticidad_dinamica if p0 > 0 else 0.0
                    a = q0 + (b * p0)

                    # El precio óptimo ahora SÍ varía según los días (a través de la sales_rate)
                    suggested_price = a / (2.0 * b) if b > 0 else p0

                    # --- RESTRICCIONES REALES DE INVENTARIO (Tu bloque de escasez) ---
                    tasa_venta_diaria = sales_rate
                    if stock > 0 and tasa_venta_diaria > 0:
                        dias_cobertura = stock / tasa_venta_diaria
                        if dias_cobertura < days:
                            factor_escasez = 1.0 + ((days - dias_cobertura) / days) * 0.5
                            suggested_price *= factor_escasez

                    # Acotaciones comerciales finales
                    suggested_price = max(p0 * 0.5, min(p0 * 2.0, suggested_price)) # Ampliado a 2.0 por si es un éxito rotundo
                    suggested_price = round(suggested_price, 2)
                    delta = round(suggested_price - p0, 2)
                    percent_change = round((delta / p0) * 100, 2) if p0 else 0.0

                    if delta > 0:
                        recommendation = 'subir'
                    elif delta < 0:
                        recommendation = 'bajar'
                    else:
                        recommendation = 'mantener'

                    inventory_days = round(stock / sales_rate, 1) if sales_rate > 0 else 0.0
                    explanation = (
                        'La optimización utiliza cálculo diferencial sobre la función de ingreso: '
                        'se estima una curva de demanda lineal, se construye el ingreso total '
                        'I(p) = p · Q(p), y se halla el máximo analizando la derivada I\'(p).' 
                    )

                    result = {
                        'product_name': form.cleaned_data['product_name'],
                        'suggested_price': suggested_price,
                        'delta': delta,
                        'percent_change': percent_change,
                        'recommendation': recommendation,
                        'inventory_days': inventory_days,
                        'days_range': days,
                        'sales_per_day': round(sales_rate, 2),
                        'explanation': explanation,
                        'coef_a': round(a, 2),
                        'coef_b': round(b, 4),
                    }

    return render(request, 'pricing_app/index.html', {'form': form, 'result': result})
