from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
from .models import *
from accounts.models import Cart , CartItems 
from django.http import HttpResponseRedirect


def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        if user_obj:
            login(request , user_obj)
            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')




def activate_email(request , email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    

def add_to_cart(request , uid):
    variant = request.GET.get('variant')

    product = Product.objects.get(uid =uid)
    user = request.user
    cart , _ = Cart.objects.get_or_create(user = user , is_paid = False)

    cart_item = CartItems.objects.create(cart = cart , product = product ,)

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name = variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_cart(request , cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid =cart_item_uid)
        cart_item.delete()
    except Exception as e:
        print(e)


    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def cart(request):
    context = {'cart' : Cart.objects.get(is_paid = False , user =  request.user)}
    return render(request , 'accounts/cart.html', context)



import requests
import json

url = "https://a.khalti.com/api/v2/epayment/initiate/"

payload = json.dumps({
    "return_url": "http://127.0.0.1:8000/",
    "website_url": "http://127.0.0.1:8000/",
    "amount": "1000",
    "purchase_order_id": "Order01",
    "purchase_order_name": "test",
    "customer_info": {
    "name": "Ram Bahadur",
    "email": "test@khalti.com",

    }
})
headers = {
    'Authorization': 'bc698f2e0eed4c43ba71c85e10d9b402',
    'Content-Type': 'application/json',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        url = "https://khalti.com/api/v2/payment/verify/"
        headers = {
            'Authorization': f'Khalti {settings.ded8608319bf417492456d20b50392b1}',  
            'Content-Type': 'application/json',
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed'})

    return JsonResponse({'status': 'invalid request'}, status=400)
