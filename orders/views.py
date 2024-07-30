from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from blog.models import Profile


@csrf_protect
def order_create(request):
    cart = Cart(request)
    initial_data = {}

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'address': profile.location,
        }

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('orders:order_created')
    else:
        form = OrderCreateForm(initial=initial_data)
    return render(request, 'orders/create.html', {'cart': cart, 'form': form})


def order_created(request):
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('cart:cart_detail')
    order = Order.objects.get(id=order_id)
    del request.session['order_id']
    return render(request, 'orders/created.html', {'order': order})
