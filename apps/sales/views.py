# my_app/views.py
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Sale, ProductSold, Customer
from apps.inventory.models import Products
from .form import CustomerForm

def register_sale_view(request):
    # CASO 1: Procesar la venta final enviada desde la rejilla (POST vía AJAX/Fetch)
    if request.method == "POST":
        try:
            # Cargamos los datos JSON enviados desde el frontend
            data = json.loads(request.body)
            
            customer_id = data.get('customer_id') # Puede ser None si es venta normal
            products_list = data.get('products', []) # Lista de productos de la rejilla
            
            # Validamos que al menos venga un producto en la rejilla
            if not products_list:
                return JsonResponse({'status': 'error', 'message': 'The product grid is empty.'}, status=400)
            
            # 1. Identificar si es cliente de fiado o venta normal
            customer = None
            if customer_id:
                customer = get_object_or_404(Customer, id=customer_id)
            
            # 2. Creamos la cabecera de la venta (Una sola Sale para todos los productos)
            new_sale = Sale.objects.create(customer=customer)
            
            # 3. Iteramos la rejilla y creamos todos los ProductSold asociados a esta Sale
            for item in products_list:
                product_obj = get_object_or_404(Products, id=item['product_id'])
                
                ProductSold.objects.create(
                    sale=new_sale,
                    product=product_obj,
                    amount_products=int(item['amount'])
                )
            
            # Si todo sale bien, respondemos con éxito
            return JsonResponse({
                'status': 'success', 
                'message': 'Sale registered successfully!',
                'sale_id': new_sale.id
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    # CASO 2: Cargar la pantalla de ventas con la rejilla limpia (GET)
    else:
        customers = Customer.objects.filter(active=True)
        products = Products.objects.all()
        
        context = {
            'customers': customers,
            'products': products
        }
        return render(request, 'register_sale.html', context)
    


def view_customers_active(request):
    if request.method == "GET":
        customers_active = Customer.objects.filter(active=True)
        return render(request, "view_customers.html", {
            "customers":customers_active,
            'es_activo': True

        })

def view_customers_deactive(request):
    if request.method == "GET":
        customers_active = Customer.objects.filter(active=False)
        return render(request, "view_customers.html", {
            "customers":customers_active,
            'es_activo': False
        })


def create_new_customer(request):
    """RECUERDA QUE ESTA FUNCION SE LLAMA AL INGRESAR AL LINK DE CREAR NUEVO PODUCTO
    POR ENDE DEBE RENDERIZAR EL FOMULARIO Y ALA VEZ CREAR EL OBJETO"""
    if request.method == "GET": #O sea para cargar el fomrmulario
        return render(request, "create_customer.html", {
            "form": CustomerForm
        })
    if request.method == "POST": #o sea que ya envio el formulario
        try:
            form = CustomerForm(request.POST)
            new_customer = form.save()
            return redirect("view_customers_active")
        except ValueError:
            return render(request, "create_customer.html", {
            "form": CustomerForm,
            "error":"los valores son erroneos"})

def update_customer(request, customer_id):
    """Busca un cliente por su ID (llave primaria) y permite editarlo"""
    # 1. Buscamos el cliente en la base de datos usando su ID
    customer = get_object_or_404(Customer, pk=customer_id)
    
    if request.method == "GET":
        # Pasamos 'instance=cliente' para que el formulario se cargue 
        # automáticamente con los datos actuales del cliente
        form = CustomerForm(instance=customer)
        return render(request, "update_customer.html", {
            "form": form,
            "customer": customer
        })
        
    if request.method == "POST":
        try:
            # Vinculamos los datos enviados con el cliente existente
            form = CustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect("view_customers")  # Redirige a la lista de clientes
        except ValueError:
            return render(request, "update_customer.html", {
                "form": form,
                "customer": customer,
                "error": "Los valores ingresados son erróneos"
            })

def delete_customer(request, customer_id):
    """Elimina un cliente de la base de datos tras una confirmación POST"""
    customer = get_object_or_404(Customer, pk=customer_id)
    
    if request.method == "POST":
        customer.delete()
        return redirect("view_customers")  # Redirige a la lista de clientes
        
    # Si entran por GET, les mostramos la página de confirmación tipo "cajita" que armamos antes
    return render(request, "delete_customer_confirmation.html", {"product": customer})




def view_sales_all(request):
    """Muestra absolutamente todas las ventas"""
    sales = Sale.objects.all()
    return render(request, "view_sales.html", {
        "sales": sales,
        "filtro_actual": "todos"  # <-- Enviamos el estado a Jinja
    })

def view_sales_normal(request):
    """Muestra solo ventas normales (donde el cliente es nulo/None)"""
    sales = Sale.objects.filter(customer__isnull=True)
    return render(request, "view_sales.html", {
        "sales": sales,
        "filtro_actual": "normal"  # <-- Enviamos el estado a Jinja
    })

def view_sales_fiado(request):
    """Muestra solo los fiados (donde sí hay un cliente asociado)"""
    sales = Sale.objects.filter(customer__isnull=False)
    return render(request, "view_sales.html", {
        "sales": sales,
        "filtro_actual": "fiado"   # <-- Enviamos el estado a Jinja
    })