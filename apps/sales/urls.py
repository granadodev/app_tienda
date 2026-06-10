from . import views
from django.urls import path

urlpatterns = [
    path("register_sale/", views.register_sale_view, name="register_sale"),
    path("customers/", views.view_customers_active, name="view_customers"),
    path("customers/active", views.view_customers_active, name="view_customers_active"),
    path("customers/deactive", views.view_customers_deactive, name="view_customers_deactive"),
    path("customers/create", views.create_new_customer, name="create_customer"),
    path("customers/details<int:customer_id>/", views.details_customer, name="details_customer"),
    path("customers/update<int:customer_id>/", views.update_customer, name="update_customer"),
    path("customers/delete<int:customer_id>/", views.delete_customer, name="delete_customer"),
    path("sales", views.view_sales_all, name="view_sales"),
    path("sales/normal", views.view_sales_normal, name="view_sales_normal"),
    path("sales/fiado", views.view_sales_fiado, name="view_sales_fiado"),
]
