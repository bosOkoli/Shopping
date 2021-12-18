from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from store.utils import cookieCart, cartData, guestOrder
from store.models import *


def register(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
          form.save()
          username = form.cleaned_data.get('username')
          messages.success(request, f'Your Account has been created. You are now able to login!')
          return redirect('login')
    else:
      form = UserRegisterForm()
    return render(request, 'user/register.html',{"form":form,"products":products,"cartItems":cartItems})


@login_required
def profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    if request.method == 'POST':
      u_form = UserUpdateForm(request.POST, instance = request.user )
      p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
      if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Your Account has been successfully updated!')
        return redirect('profile')
    else:
      u_form = UserUpdateForm(instance = request.user )
      p_form = ProfileUpdateForm(instance = request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        "products":products,
        "cartItems":cartItems
      }
    return render(request, 'user/profile.html', context)
