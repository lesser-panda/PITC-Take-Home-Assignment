from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.decorators import login_required


@login_required
def welcome_view(request):
    return render(request, 'customer_portal.html')


class CustomerLoginView(LoginView):
    template_name = 'customer_login.html'
    
    def form_valid(self, form):
        if form.get_user().role != 'customer':
            return self.form_invalid(form)
        return super().form_valid(form)


class OrderList(View):
    def get(self, request):
        return render(
            request,
            'customer_order_list.html',
            {'orders': request.user.customer_profile.orders.all()}
        )


class OrderDetail(View):
    def get(self, request, order_id):
        order = request.user.customer_profile.orders.get(id=order_id)
        return render(
            request,
            'customer_order_detail.html',
            {'order': order}
        )
