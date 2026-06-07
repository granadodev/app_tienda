from django.db import models
from django.db.models import Sum
from apps.inventory.models import Products  # Ajusta esta ruta según tu proyecto

class Customer(models.Model):
    name = models.CharField(max_length=250, verbose_name="Nombre")
    number_phone = models.CharField(max_length=20, verbose_name="Teléfono")
    mail = models.EmailField(unique=True, blank=True, null=True, verbose_name="Correo Electrónico")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    
    date_register = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, help_text="Indica si el cliente puede seguir pidiendo fiado")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.number_phone})"


class Sale(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, null=True, blank=True, default=None, on_delete=models.CASCADE)

    @property
    def total_price(self):
        """Suma el 'price_total' de todos los productos vendidos en esta venta."""
        resultado = self.productsold_set.aggregate(total=Sum('price_total'))
        return resultado['total'] if resultado['total'] else 0.00

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-date']

    def __str__(self):
        return f"Venta N° {self.id} - {self.customer.name if self.customer else 'Anónimo'} - Total: ${self.total_price}"

class ProductSold(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.PROTECT) 
    amount_products = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    
    # editable=False evita que el campo aparezca en formularios o en el admin de Django
    price_by = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False, verbose_name="Precio Unitario")
    price_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, editable=False, verbose_name="Precio Total")

    class Meta:
        verbose_name = "Producto Vendido"
        verbose_name_plural = "Productos Vendidos"

    def save(self, *args, **kwargs):
        """Bloqueado: Siempre extrae el precio oficial del inventario y calcula el total."""
        # No importa lo que venga de afuera, aquí se fuerza el precio del producto del inventario
        self.price_by = self.product.price_by  
        
        # Se calcula el total con ese precio oficial
        self.price_total = self.amount_products * self.price_by
        
        super(ProductSold, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.amount_products}x {self.product.name} (Total: ${self.price_total})"