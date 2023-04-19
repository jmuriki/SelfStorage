from django.shortcuts import render


def index(request):
	return render(request, 'index.html')


def tariffs(request):
	return render(request, 'tariffs.html')


def calculator(request):
	return render(request, 'calculator.html')


def rent_box(request):
	return render(request, 'boxes.html')


def can_be_stored(request):
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


def sign_up(request):
	return render(request, 'sign_up.html')


def sign_in(request):
	return render(request, 'sign_in.html')


def restore(request):
	return render(request, 'restore.html')


# def #(request):
# 	return render(request, '#.html')
