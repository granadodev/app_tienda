from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductosForm
from .models import Products

# Create your views here.
def view_inventory(request):
    if request.method == "GET":
        products = Products.objects.all()
        return render(request, 'view_inventory.html', {
            "products":products
        })
    
def create_new_products(request):
    """RECUERDA QUE ESTA FUNCION SE LLAMA AL INGRESAR AL LINK DE CREAR NUEVO PODUCTO
    POR ENDE DEBE RENDERIZAR EL FOMULARIO Y ALA VEZ CREAR EL OBJETO"""
    if request.method == "GET": #O sea para cargar el fomrmulario
        return render(request, "create_inventory.html", {
            "form": ProductosForm
        })
    if request.method == "POST": #o sea que ya envio el formulario
        try:
            form = ProductosForm(request.POST)
            new_product = form.save()
            return redirect("view_inventory")
        except ValueError:
            return render(request, "create_inventory.html", {
            "form": ProductosForm,
            "error":"los valores son erroneos"})


def update_product(request, product_id):
    """Busca un producto por su nombre (llave primaria) y permite editarlo"""
    # 1. Buscamos el producto en la base de datos usando su nombre
    producto = get_object_or_404(Products, pk=product_id)
    
    if request.method == "GET":
        # Pasamos 'instance=producto' para que el formulario se cargue 
        # automáticamente con los datos actuales del producto
        form = ProductosForm(instance=producto)
        return render(request, "update_inventory.html", {
            "form": form,
            "producto": producto
        })
        
    if request.method == "POST":
        try:
            # Vinculamos los datos enviados con el producto existente
            form = ProductosForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return redirect("view_inventory")
        except ValueError:
            return render(request, "update_inventory.html", {
                "form": form,
                "producto": producto,
                "error": "Los valores son erróneos"
            })

def delete_product(request, product_id):
    """Elimina un producto de la base de datos tras una confirmación POST"""
    producto = get_object_or_404(Products, pk=product_id)
    
    if request.method == "POST":
        producto.delete()
        return redirect("view_inventory")
        
    # Si entran por GET, les mostramos una página de confirmación "¿Estás seguro?"
    return render(request, "delete_confirmation.html", {"product": producto})

