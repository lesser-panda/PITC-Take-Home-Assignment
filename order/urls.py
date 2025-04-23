from django.urls import path, include

from order import views as order_views


urlpatterns = [
    path('customer_login/', order_views.CustomerLoginView.as_view(), name='customer_login'),
    path('customer_portal/', order_views.welcome_view, name='customer_portal'),
    path('customer_portal/orders/', order_views.OrderList.as_view(), name='customer_order_list'),
]
