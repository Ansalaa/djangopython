from django.shortcuts import render, redirect

from shop.models import Product
from cart.models import Cart, Order_details, Payment

import razorpay


def addcart(request, i):
    p = Product.objects.get(id=i)
    u = request.user

    try:
        c = Cart.objects.get(user=u, product=p)  # if product is already present inside table for the current user
        c.quantity += 1  # it will increment the quantity inside the record
        p.stock -= 1
        p.save()
        c.save()

    except:  # if not present
        c = Cart.objects.create(user=u, product=p, quantity=1)  # it will add a new record with quantity =1
        p.stock -= 1
        p.save()
        c.save()

    return redirect('cart:cartview')


def cart_view(request):
    u = request.user
    c = Cart.objects.filter(user=u)
    totel = 0
    for i in c:
        totel += i.quantity * i.product.price
    context = {'cart': c, 'totel': totel}
    return render(request, 'cart.html', context)


def cart_remove(request, i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(user=u, product=p)
        if (c.quantity > 1):  # if quantity > 0
            c.quantity -= 1
            c.save()
            p.stock += 1
            p.save()
        else:  # if cart quantity = 0
            c.delete()
            p.stock += 1
            p.save()
    except:
        pass
    return redirect('cart:cartview')


def cart_delete(request, i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(user=u, product=p)
        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass

    return redirect('cart:cartview')


def orderform(request):
    if request.method == "POST":
        a = request.POST['a']
        p = request.POST['p']
        n = request.POST['n']

        u = request.user
        c = Cart.objects.filter(user=u)

        total = 0
        for i in c:
            total += i.product.price * i.quantity

        print(total)

        # Razorpay connemction
        client = razorpay.Client(auth=('rzp_test_64QMU042Xkyl5V', 'ccRXcmzCs68MZULI0vKtxdua'))

        # Razorpay order creation
        response_payment = client.order.create(dict(amount=total * 100, currency='INR'))
        order_id = response_payment['id']  # Retrieve the order id from response
        status = response_payment['status']  # Retrieve the status from response

        if (status == "created"):
            s = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            s.save()

            for i in c:
                o = Order_details.objects.create(product=i.product, user=i.user, phone=p, address=a, pin=n,
                                                 order_id=order_id, no_of_items=i.quantity)
                o.save()

            context = {'payment': response_payment, 'name': u.username}
            return render(request, 'payment.html', context)  # Send the response from view to payment.html

    return render(request, 'oredrform.html')


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login


@csrf_exempt
def payment_status(request, p):
    user = User.objects.get(username=p)  # retriev user objec
    login(request, user)

    response = request.POST  # razorpay response after successfull payment
    print(response)

    # to check the validity(authenticity) of razorpay detailes received by application
    param_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],
    }

    client = razorpay.Client(auth=('rzp_test_64QMU042Xkyl5V', 'ccRXcmzCs68MZULI0vKtxdua'))

    try:
        status = client.utility.verify_payment_signature(param_dict)
        print(status)

        p = Payment.objects.get(order_id=response[
            'razorpay_order_id'])  # after successfull payment retrieve the payment record maatching with order_id=response['order_id']
        p.razorpay_payment_id = response[
            'razorpay_payment_id']  # assigns response payment is to razorpay id to razorpay_payment_id
        p.paid = True  # assign paid value to true
        p.save()

        o = Order_details.objects.filter(order_id=response[
            'razorpay_order_id'])  # after successfull payment retrieve the order_details record maatching with order_id=response['order_id']
        for i in o:
            i.payment_status = "completed"
            i.save()

        # to remove cart items for a perticular user after successfull payment
        c = Cart.objects.filter(user=user)
        c.delete()

    except:
        pass

    return render(request, 'payment_status.html')


def orderview(request):
    u = request.user
    o = Order_details.objects.filter(user=u, payment_status="completed")
    context = {'orders': o}
    return render(request, 'orderview.html', context)