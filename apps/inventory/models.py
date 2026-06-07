from django.db import models

# Create your models here.
class Products(models.Model):

    UNIT_MEASUREMENT_CHOICE = [
        ("unidad", "Unidad"),
        ("libra", "Libra"),
        ("kilo", "Kilo"),
        ("gramo", "Gramo"),

    ]
    
    name = models.TextField(unique=True)
    stock = models.IntegerField(default=1)
    unit_measurement = models.TextField(choices=UNIT_MEASUREMENT_CHOICE, default=0)
    price_by = models.IntegerField()

    class Meta():
        db_table = "productos"
        verbose_name = "Productos"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name