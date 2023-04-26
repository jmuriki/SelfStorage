import os
import qrcode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from storage_rental.models import Customer, Storage, Cell, Order
from django.dispatch import receiver

from functools import wraps
from yookassa import Configuration, Payment
from selfstorage.settings import PAY_ACC, PAY_KEY
from urllib.parse import urlparse


def save_to_cookies(request, key, payload):
    request.session[key] = payload
    request.session.modified = True
    response = HttpResponse("Your choice was saved as a cookie!")
    response.set_cookie('session_id', request.session.session_key)
    return


def if_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request, context={}, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            context['customer'] = customer
            return view_func(request, context, *args, **kwargs)
        else:
            return view_func(request, context, *args, **kwargs)
    return wrapper


@if_authenticated
def rent_box(request, context={}):
    all_free_cells = Cell.objects.with_square().filter(occupied=False)
    to3_free_cells = Cell.objects.with_square().filter(occupied=False).filter(sq__lte=3)
    to10_free_cells = Cell.objects.with_square().filter(occupied=False).filter(sq__lte=10)
    from10_free_cells = Cell.objects.with_square().filter(occupied=False).filter(sq__gt=10)
    cells_payload = [
        { 
            "cell_size": "all",
            "cells": all_free_cells,
        },
        {
            "cell_size": "to3",
            "cells": to3_free_cells,
        },
        {
            "cell_size": "to10",
            "cells": to10_free_cells,
        },
        {
            "cell_size": "from10",
            "cells": from10_free_cells,
        },
    ]
    storages = Storage.objects.with_all_cells_filters().prefetch_related('cells')
    context['cells_payload'] = cells_payload
    context['storages'] = storages
    return render(request, 'rent_box.html', context)


@if_authenticated
def index(request, context=None):
    return render(request, 'index.html', context)


@if_authenticated
def tariffs(request, context=None):
    return render(request, 'tariffs.html', context)


@if_authenticated
def calculator(request, context=None):
    return render(request, 'calculator.html', context)


@if_authenticated
def faq(request, context=None):
    return render(request, 'faq.html', context)


@if_authenticated
def locations(request, context=None):
    return render(request, 'locations.html', context)


@if_authenticated
def contacts(request, context=None):
    return render(request, 'contacts.html', context)


@if_authenticated
def customers_reviews(request, context=None):
    return render(request, 'customers_reviews.html', context)


@if_authenticated
def privacy_policy(request, context=None):
    return render(request, 'privacy_policy.html', context)


@if_authenticated
def documents(request, context=None):
    return render(request, 'documents.html', context)


@if_authenticated
def notifications(request, context=None):
    if context:
        return render(request, 'notifications.html', context)
    return redirect('main_page')


@if_authenticated
def account(request, context=None):
    user_id = request.user.id
    customer = Customer.objects.get(id=user_id)
    cell_id = request.session.get('cell_id', None)
    if cell_id:
        cell = Cell.objects.get(id=cell_id)
        new_order = Order.objects.create(customer=customer, status='created')
        new_order.cells.add(cell)
        new_order.save()
        save_to_cookies(request, 'cell_id', None)
    if context:
        context['customer'] = Customer.objects.prefetch_related('orders').get(id=user_id)
        context['created_orders'] = Order.objects.filter(status='created', customer=customer)
        context['payed_orders'] = Order.objects.filter(status='payed', customer=customer)
        return render(request, 'account.html', context)
    return redirect('main_page')


def sign_up(request, context={}):
    if request.method == 'POST':
        username = request.POST['EMAIL_CREATE']
        password = request.POST['PASSWORD_CREATE']
        confirm_password = request.POST['PASSWORD_CONFIRM']

        if User.objects.filter(username=username).exists():
            context['error'] = """Такой пользователь уже зарегистрирован.
            Если вы не помните свой пароль, сделайте запрос на восстановление."""
            return render(request, 'sign_up.html', context)
        elif password == confirm_password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('account')
        else:
            context['sign_up'] = False
            context['error'] = 'Пароли не совпадают. Пожалуйста, попробуйте снова.'
            return render(request, 'sign_up.html', context)
    else:
        need_sign_up = request.session.get('need_sign_up')
        if need_sign_up:
            context['sign_up'] = True
            save_to_cookies(request, 'need_sign_up', False)
        return render(request, 'sign_up.html', context)


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance, email=instance)


def sign_in(request, context={}):
    if request.method == 'POST':
        username = request.POST.get('EMAIL')
        password = request.POST.get('PASSWORD')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('account')
        else:
            context['error'] = 'Неверный логин или пароль'
            return render(request, 'sign_in.html', context)
    else:
        context['error'] = 'Ошибка: неверный тип запроса.'
        return render(request, 'sign_in.html', context)


def sign_out(request):
    logout(request)
    return redirect('main_page')


def restore(request):
    return render(request, 'restore.html')


@login_required
def change_user_info(request):
    user = request.user
    if request.method == 'POST':
        customer = Customer.objects.get(user=request.user)
        if customer:
            customer.first_name = request.POST.get('NAME_EDIT')
            customer.last_name = request.POST.get('SURNAME_EDIT')
            customer.phone_number = request.POST.get('PHONE_EDIT')
            customer.email = request.POST.get('EMAIL_EDIT')
            if request.FILES.get('AVATAR_EDIT'):
                customer.avatar = request.FILES.get('AVATAR_EDIT')
            customer.save()
        new_password = request.POST.get('PASSWORD_EDIT')
        if new_password:
            user.set_password(new_password)
            user.save()
            return redirect('main_page')
    return redirect('account')


@login_required
def payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        cell_id = request.POST.get('cell_id')
        summa = request.POST.get('summa')
        descr = request.POST.get('descr')
        save_to_cookies(request, 'payed_cell_id', cell_id)
        save_to_cookies(request, 'payed_order_id', order_id)
    summa = 153.42
    descr = "Описание предмета платежа"
    absolute_url = request.build_absolute_uri()
    parsed_url = urlparse(absolute_url)
    ret_url = f'{parsed_url.scheme}://{parsed_url.netloc}/pay_result?payment_success=1'
    yookassa = make_pay(PAY_ACC, PAY_KEY, summa, descr, ret_url)
    return redirect(yookassa.confirmation.confirmation_url)

@if_authenticated
def pay_result(request, context={}):
    payment_res = request.GET['payment_success']
    message = "Оплата не прошла."
    if payment_res:
        message = "Оплата прошла успешно."
        payed_order_id = request.session.get('payed_order_id')
        payed_order = Order.objects.get(id=payed_order_id)
        payed_order.status = 'payed'
        payed_order.save()
        save_to_cookies(request, 'payed_cell_id', None)
        save_to_cookies(request, 'payed_order_id', None)
    context['payment_res'] = message

    return render(request, 'pay_result.html', context)


def make_pay(pay_account, pay_secretkey, summa, descr, ret_url):
    Configuration.account_id = pay_account
    Configuration.secret_key = pay_secretkey

    return Payment.create({
        "amount": {
            "value": summa,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": ret_url
        },
        "capture": True,
        "description": descr
    })


@login_required
def qr(request):
    if request.method == 'POST':
        qr_cell_id = request.POST.get('qr_cell_id')
        qr_data = f"Это qr-код для открытия ячейки № {qr_cell_id}"
        name, _ = str(request.user).split("@")
        qr_name = create_qr_code(name, qr_data)
        context = {'qrcode': qr_name}
    return render(request, 'qr.html', context)


def create_qr_code(name, data):
    qr_name = f'{name}.png'
    qr_path = os.path.join(settings.BASE_DIR, 'media', qr_name)
    qrcode.make(data).save(qr_path)
    return qr_name


@if_authenticated
def make_order(request, context=None):
    if request.method == 'POST':
        cell_id = request.POST.get('cell_id')
        save_to_cookies(request, 'cell_id', cell_id)
        if not context:
            save_to_cookies(request, 'need_sign_up', True)
            return redirect('sign_up')
        return redirect('account')
    return redirect('main_page')
