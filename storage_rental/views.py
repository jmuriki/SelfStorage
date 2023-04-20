from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def index(request):
	# is_authenticated = request.user.is_authenticated
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'index.html', context)


def tariffs(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'tariffs.html', context)


def calculator(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'calculator.html', context)


def rent_box(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'boxes.html', context)


def can_be_stored(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'faq.html', context)


def locations(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'locations.html', context)


def contacts(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'contacts.html', context)


def customers_reviews(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'customers_reviews.html', context)


def privacy_policy(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'privacy_policy.html', context)


def documents(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'documents.html', context)


def account(request):
	is_authenticated = True
	context = {'is_authenticated': is_authenticated}
	return render(request, 'account.html', context)


def sign_up(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'sign_up.html', context)


def sign_in(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'sign_in.html', context)


def restore(request):
	is_authenticated = False
	context = {'is_authenticated': is_authenticated}
	return render(request, 'restore.html', context)
