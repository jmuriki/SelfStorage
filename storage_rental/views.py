from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth


def index(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'index.html', context)


def tariffs(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'tariffs.html', context)


def calculator(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'calculator.html', context)


def rent_box(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'rent_box.html', context)


def faq(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'faq.html', context)


def locations(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'locations.html', context)


def contacts(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'contacts.html', context)


def customers_reviews(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'customers_reviews.html', context)


def privacy_policy(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'privacy_policy.html', context)


def documents(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'documents.html', context)


def account(request):
	is_authenticated = request.user.is_authenticated
	context = {
		'is_authenticated': is_authenticated,
	}

	if is_authenticated:
		return render(request, 'account.html', context)
	return redirect('main_page')


def sign_up(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}

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
			context['error'] = 'Пароли не совпадают. Пожалуйста, попробуйте снова.'
			return render(request, 'sign_up.html', context)
	else:
		context['error'] = 'Ошибка: неверный тип запроса.'
		return render(request, 'sign_up.html', context)


def sign_in(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}

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
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	return render(request, 'restore.html', context)


@login_required
def change_user_info(request):
	is_authenticated = request.user.is_authenticated
	context = {'is_authenticated': is_authenticated}
	if request.method == 'POST':
		user = request.user
		user.email = request.POST.get('EMAIL_EDIT')
		user.phone_number = request.POST.get('PHONE_EDIT')
		new_password = request.POST.get('PASSWORD_EDIT')
		if new_password:
			user.set_password(new_password)
		user.save()
		return redirect('account')
	return redirect('account')
