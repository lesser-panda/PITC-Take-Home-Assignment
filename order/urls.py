from django.urls import path

from order import views as order_views


urlpatterns = [
    path('customer_login/', order_views.CustomerLoginView.as_view(), name='customer_login'),
    path('customer_portal/', order_views.welcome_view, name='customer_portal'),
    path('customer_portal/orders/', order_views.OrderList.as_view(), name='customer_order_list'),
    path('customer_portal/orders/<int:order_id>/', order_views.OrderDetail.as_view(), name='customer_order_detail'),
    path('customer_portal/orders/<int:order_id>/available_to_add/', order_views.list_available_products_services, name='customer_order_available_items_to_add'),
    path('customer_portal/orders/add_items/', order_views.add_product_or_service_to_order, name='customer_order_add_items'),
]
