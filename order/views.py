from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from order.forms import CustomerOrderForm
from order import models as order_models
from registrar import models as registrar_models


def homepage(request):
    """Landing page when the user is not logged in."""
    if request.user.is_authenticated:
        if request.user.role == 'customer':
            return redirect('customer_portal')
        else:
            return redirect('/admin')
    return render(request, 'home.html')


@login_required
def welcome_view(request):
    return render(request, 'customer_portal.html')


class CustomerLoginView(LoginView):
    template_name = 'customer_login.html'
    
    def form_valid(self, form):
        if form.get_user().role != 'customer':
            return self.form_invalid(form)
        return super().form_valid(form)


class OrderList(LoginRequiredMixin, View):
    """View for customers to view and create orders."""
    def get(self, request):
        return render(
            request,
            'customer_order_list.html',
            {'orders': request.user.customer_profile.orders.all()}
        )
    
    def post(self, request):
        """Create a new order by selecting an account manager."""
        customer = request.user.customer_profile
        form = CustomerOrderForm(request.POST, customer=customer)

        if form.is_valid():
            order = form.save(commit=False)
            order.customer = customer
            order.save()
            return redirect('customer_order_list')
        else:
            orders = customer.orders.all()
            return render(
                request,
                'customer_order_list.html',
                {'orders': orders, 'form': form}
            )


class OrderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = request.user.customer_profile.orders.get(id=order_id)
        return render(
            request,
            'customer_order_detail.html',
            {'order': order}
        )
        

@login_required
def list_available_products_services(request, order_id):
    order = request.user.customer_profile.orders.get(id=order_id)
    service_provider_ids = registrar_models.AccountManagerServiceProvider.objects.filter(
        account_manager=order.account_manager
    ).values_list('service_provider_id', flat=True)
    products_and_services = order_models.ProductAndService.objects.filter(
        service_provider_id__in=service_provider_ids
    )
    return render(
        request,
        'partials/products_and_services_selection.html',
        {
            'order': order,
            'products_and_services': products_and_services,
        }
    )

@login_required
def add_product_or_service_to_order(request):
    order = request.user.customer_profile.orders.get(id=request.POST.get('order_id'))
    item = order_models.ProductAndService.objects.get(id=request.POST.get('product_service_id'))
    order_models.OrderItem.objects.create(
        order=order,
        product=item,
        quantity=request.POST.get('quantity', 1)
    )
    order.refresh_from_db()
    return render(
        request,
        'partials/products_and_services_list.html',
        {'order': order}
    )
