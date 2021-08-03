# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from orders.models import Order
from zeep import Client


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
client = Client('http://sandbox.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://127.0.0.1:8000/zarinpal/verify/' # Important: need to edit for realy server.

def get_user_detail(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    amount = order.get_total_cost()
    description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
    email = order.email
    mobile = '09123456789'  # Optional
    return {'amount': amount,
            'description': description,
            'email': email,
            'mobile': mobile,
            'order': order}

def send_request(request):
    details = get_user_detail(request)
    result = client.service.PaymentRequest(MERCHANT,
                                           details['amount'],
                                           details['description'],
                                           details['email'],
                                           details['mobile'],
                                           CallbackURL)
    if result.Status == 100:
        return redirect('http://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))

    else:
        return HttpResponse('Error code: ' + str(result.Status))

def verify(request):
    details = get_user_detail(request)
    amount = details['amount']
    order = details['order']

    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.zarinpal_id = str(request.GET.get('Authority'))
            order.save()
            return redirect('zarinpal:done')
            # return HttpResponse('Transaction success.\nRefID: ' + str(result.RefID))

        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))

        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status))


    return redirect('zarinpal:canceled')
    # else:
    #     # generate token
    #     client_token = client.personal_token.generate()
    #     return render(request,
    #         'zarinpal/request/',
    #         {'order': order,
    #         'client_token': client_token})
    # else:
    #     return HttpResponse('Transaction failed or canceled by user')

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
