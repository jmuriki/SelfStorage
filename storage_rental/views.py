from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from storage_rental.models import Customer
from django.contrib import auth
from functools import wraps


def if_authenticated(view_func):
    @wraps(view_func)
    def wrapper(request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(login=request.user)
            context = {'customer': customer}
            return view_func(request, context=context)
        else:
            return view_func(request)
    return wrapper


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
def rent_box(request, context=None):
	return render(request, 'rent_box.html', context)


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
def account(request, context=None):
	if context:
		return render(request, 'account.html', context)
	return redirect('main_page')


@if_authenticated
def notifications(request, context=None):
	if context:
		return render(request, 'notifications.html', context)
	return redirect('main_page')


def sign_up(request):
	context = {}
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
			Customer.objects.create(login=user)
			login(request, user)
			return redirect('account')
		else:
			context['error'] = 'Пароли не совпадают. Пожалуйста, попробуйте снова.'
			return render(request, 'sign_up.html', context)
	else:
		context['error'] = 'Ошибка: неверный тип запроса.'
		return render(request, 'sign_up.html', context)


def sign_in(request):
	context = {}
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
		
		customer = Customer.objects.get(login=request.user)
		if customer:
			customer.name = request.POST.get('NAME_EDIT')
			customer.surname = request.POST.get('SURNAME_EDIT')
			customer.phone_number = request.POST.get('PHONE_EDIT')
			customer.email = request.POST.get('EMAIL_EDIT')
			customer.save()

		new_password = request.POST.get('PASSWORD_EDIT')
		if new_password:
			user.set_password(new_password)
		user.save()
		return redirect('account')
	return redirect('account')


@login_required
def payment(request):
	payment = None
	message = "Оплата не прошла."
	if payment:
		message = "Оплата прошла успешно."
	context = {'payment_result': message}
	return render(request, 'payment.html', context)
