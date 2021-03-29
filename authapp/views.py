from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserRegistration, UserEditForm, OrderModelForm, OrderModelFormEdit
from decimal import Decimal
from fractions import *
from .models import OrderModel
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required
def dashboard(request):
    current_user = request.user
    my_orders = OrderModel.objects.filter(customer=current_user).order_by('-order_date')

    page = request.GET.get('page', 1)
    paginator = Paginator(my_orders, 4)

    try:
        my_orders = paginator.page(page)
    except PageNotAnInteger:
        my_orders = paginator.page(1)
    except EmptyPage:
        my_orders = paginator.page(paginator.num_pages)

    context = { 'my_orders': my_orders }

    return render(request, 'authapp/dashboard.html', context=context)


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            return render(request, 'authapp/register_done.html')
    else:
        form = UserRegistration()

    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)


@login_required
def order(request):
    if request.method == 'POST':
        form = OrderModelForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=True)
            area = order.width * order.height
            area_feet = Decimal(area)/Decimal(144)
            order.total_price = round(Decimal(area_feet) * Decimal(order.quantiy) * Decimal(120) + Decimal(150), 2)
            print(order.total_price)
            order.customer = request.user
            order.save()
            form = OrderModelForm()
            return redirect('/dashboard')
    else:
        form = OrderModelForm()
    return render(request, 'authapp/order_form.html', {
        'form': form
    })


@user_passes_test(lambda u: u.is_superuser)
def order_list(request):

    query = request.GET.get('q', '')
    # orders = OrderModel.objects.order_by('-order_date')
    orders = OrderModel.objects.filter(Q(id__icontains=query)).distinct().order_by('-order_date')

    page = request.GET.get('page', 1)
    paginator = Paginator(orders, 9)

    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = { 'orders': orders }

    return render(request, "authapp/orders.html", context)


@user_passes_test(lambda u: u.is_superuser)
def order_detail(request, id):
    order_detail = OrderModel.objects.get(id=id)
    context = { 'order_detail': order_detail }

    return render(request, "authapp/order_detail.html", context)


@user_passes_test(lambda u: u.is_superuser)
def order_edit(request, id):
    order = OrderModel.objects.get(id=id)

    if request.method == 'POST':
        form = OrderModelFormEdit(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=True)
            area = order.width * order.height
            area_feet = Decimal(area)/Decimal(144)
            order.total_price = round(Decimal(area_feet) * Decimal(order.quantiy) * Decimal(120) + Decimal(150), 2)
            order.save()
            form = OrderModelFormEdit()
            return redirect('/orders')
    else:
        form = OrderModelFormEdit(instance=order)
    return render(request, 'authapp/order_edit_form.html', {
        'form': form,
        'order': order,
    })



def my_order_detail(request, id):
    if request.user:
        # my_order_detail = OrderModel.objects.get(id=id, customer=request.user)
        my_order_detail = get_object_or_404(OrderModel, id=id, customer=request.user)
        context = { 'my_order_detail': my_order_detail }

        return render(request, "authapp/my_order_detail.html", context)
