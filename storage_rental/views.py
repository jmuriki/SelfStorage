from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from storage_rental.models import Customer
from django.contrib import auth


def index(request):
	if request.user.is_authenticated:
		customer = Customer.objects.get(userid=request.user.id)
		context = {'customer': customer}
		return render(request, 'index.html', context)
	return render(request, 'index.html')


def tariffs(request):
	return render(request, 'tariffs.html')


def calculator(request):
	return render(request, 'calculator.html')


def rent_box(request):
	return render(request, 'rent_box.html')


def faq(request):
	return render(request, 'faq.html')


def locations(request):
	return render(request, 'locations.html')


def contacts(request):
	return render(request, 'contacts.html')


def customers_reviews(request):
	return render(request, 'customers_reviews.html')


def privacy_policy(request):
	return render(request, 'privacy_policy.html')


def documents(request):
	return render(request, 'documents.html')


def account(request):
	if request.user.is_authenticated:
		customer = Customer.objects.get(userid=request.user.id)
		context = {'customer': customer}
		return render(request, 'account.html', context)
	return redirect('main_page')


def notifications(request):
	if request.user.is_authenticated:
		return render(request, 'notifications.html')
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
			Customer.objects.create(userid=user.id, email=user)
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
		
		customer = Customer.objects.get(userid=user.id)
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
