import os
import qrcode
import calendar

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
from django.core.exceptions import ObjectDoesNotExist

from functools import wraps
from datetime import datetime, timedelta
from yookassa import Configuration, Payment
from selfstorage.settings import PAY_ACC, PAY_KEY
from urllib.parse import urlparse


def save_to_cookies(request, key, payload):
    request.session[key] = payload
    request.session.modified = True
    response = HttpResponse("Your choice was saved as a cookie!")
    response.set_cookie('session_id', request.session.session_key)
    return response


def if_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request, context={}, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                customer = Customer.objects.get(user=request.user)
                context['customer'] = customer
            except ObjectDoesNotExist:
                pass
            return view_func(request, context, *args, **kwargs)
        else:
            return view_func(request, context, *args, **kwargs)
    return wrapper


@if_authenticated
def rent_box(request, context={}):
    all_free_cells = Cell.objects.with_square()\
        .filter(occupied=False)
    to3_free_cells = Cell.objects.with_square()\
        .filter(occupied=False).filter(sq__lte=3)
    to10_free_cells = Cell.objects.with_square()\
        .filter(occupied=False).filter(sq__lte=10)
    from10_free_cells = Cell.objects.with_square()\
        .filter(occupied=False).filter(sq__gt=10)
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
    storages = Storage.objects.with_all_cells_filters()\
        .prefetch_related('cells')
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


def get_dates(date_from=None):
    if not date_from:
        today = datetime.today().date()
        date_from = today
    days_in_month = calendar.monthrange(date_from.year, date_from.month)[1]
    after_month = date_from + timedelta(days=days_in_month - 1)
    return date_from, after_month


@if_authenticated
def account(request, context={}):
    user_id = request.user.id
    cell_id = request.session.get('cell_id', None)
    try:
        customer = Customer.objects.get(id=user_id)
    except ObjectDoesNotExist:
        customer = None
    if customer:
        try:
            created_orders = Order.objects.filter(
                status='created',
                customer=customer,
            ).prefetch_related('cells')
            cells_bunches = [order.cells.all() for order in created_orders]
            chousen_cells_ids = [
                cell.id for cells_bunch in cells_bunches for cell in cells_bunch
            ]
            is_chousen = int(cell_id) in chousen_cells_ids
        except AttributeError:
            is_chousen = False
        except TypeError:
            is_chousen = False
    if cell_id and customer and not is_chousen:
        cell = Cell.objects.get(id=cell_id)
        save_to_cookies(request, 'cell_id', None)
        if not cell.occupied:
            date_from, after_month = get_dates()
            new_order = Order.objects.create(
                customer=customer,
                status='created',
                date_from=date_from,
                date_to=after_month,
            )
            new_order.cells.add(cell)
            new_order.save()
        else:
            context['error'] = "Извините, данную ячейку только что арендовали."
            return render(request, 'notifications.html', context)
    if context and customer:
        today, _ = get_dates() 
        context['customer'] = Customer.objects\
            .prefetch_related('orders').get(id=user_id)
        context['created_orders'] = Order.objects\
            .filter(status='created', customer=customer)
        context['payed_orders'] = Order.objects\
            .filter(status='payed', date_to__gte=today, customer=customer)
        overdue_orders = Order.objects\
            .filter(status='payed', date_to__lt=today, customer=customer)
        for order in overdue_orders:
            order.status = 'overdue'
            order.save()
        context['overdue_orders'] = Order.objects\
            .filter(status='overdue', customer=customer)
        return render(request, 'account.html', context)
    return redirect('main_page')


def sign_up(request, context={}):
    if request.method == 'POST':
        username = request.POST['EMAIL_CREATE']
        password = request.POST['PASSWORD_CREATE']
        confirm_password = request.POST['PASSWORD_CONFIRM']

        if User.objects.filter(username=username).exists():
            context['error'] = """Такой пользователь уже зарегистрирован.
            Если вы не помните свой пароль,
            сделайте, пожалуйста, запрос на восстановление."""
            return render(request, 'sign_up.html', context)
        elif password == confirm_password:
            user = User.objects.create_user(
                username=username,
                password=password,
            )
            login(request, user)
            return redirect('account')
        else:
            context['sign_up'] = False
            context['error'] = """Пароли не совпадают.
            Пожалуйста, попробуйте снова."""
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
def payment(request, context={}):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        cell_id = request.POST.get('cell_id')
        summa = float(request.POST.get('summa').replace(",", "."))
        descr = request.POST.get('descr')
        overdue = request.POST.get('overdue')
        if overdue:
            order = Order.objects.get(id=order_id)
            start_date = order.date_from
        else:
            start_date = None
        date_from, after_month = get_dates(start_date)
        descr = f"{descr} {date_from} - {after_month}."
        cell = Cell.objects.get(id=cell_id)
        if not cell.occupied or overdue:
            save_to_cookies(request, 'payed_cell_id', cell_id)
            save_to_cookies(request, 'payed_order_id', order_id)
            absolute_url = request.build_absolute_uri()
            parsed_url = urlparse(absolute_url)
            ret_url = f'{parsed_url.scheme}://{parsed_url.netloc}/pay_result?payment_success=1'
            yookassa = make_pay(PAY_ACC, PAY_KEY, summa, descr, ret_url)
            return redirect(yookassa.confirmation.confirmation_url)
        else:
            order = Order.objects.get(id=order_id)
            order.cells.remove(cell)
            context['error'] = "Извините, данную ячейку уже арендовали."
            return render(request, 'notifications.html', context)
    return redirect('account')


@if_authenticated
def pay_result(request, context={}):
    payment_res = request.GET['payment_success']
    message = "Оплата не прошла."
    if payment_res:
        message = "Оплата прошла успешно."
        payed_cell_id = request.session.get('payed_cell_id')
        payed_cell = Cell.objects.get(id=payed_cell_id)
        payed_cell.occupied = True
        payed_cell.save()
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
        cell = Cell.objects.get(id=qr_cell_id)
        order = cell.orders.filter(status='payed').first()
        qr_data = f"""Заказ № {order.id}. Ячейка № {cell.cell_number}.
        Период аренды с {order.date_from} по {order.date_to}."""
        name = str(request.user).replace("@", "_")
        qr_name = create_qr_code(name, qr_data)
        context = {
            'qrcode': qr_name,
            'qr_details': qr_data,
            'customer': order.customer
        }
    else:
        context = {'error': "Что-то пошло не так..."}
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


@if_authenticated
def order_canсel(request, context={}):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        Order.objects.get(id=order_id).delete()
    return redirect('account')
