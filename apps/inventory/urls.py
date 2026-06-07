from . import views
from django.urls import path

urlpatterns = [
    path("inventory/", views.view_inventory, name="view_inventory"),
    path("inventory/create", views.create_new_products, name="create_products"),
    path("inventory/update/<int:product_id>/", views.update_product, name="update_product"),
    path("inventory/delete/<int:product_id>/", views.delete_product, name="delete_product"),
]
