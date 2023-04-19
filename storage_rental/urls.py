from django.urls import path
from storage_rental import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('tariffs/', views.tariffs, name='tariffs'),
    path('calculator/', views.calculator, name='calculator'),
    path('rent_box/', views.rent_box, name='rent_box'),
    path('can_be_stored/', views.can_be_stored, name='can_be_stored'),
    path('locations/', views.locations, name='locations'),
    path('contacts/', views.contacts, name='contacts'),
    path('customers_reviews/', views.customers_reviews, name='customers_reviews'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('documents/', views.documents, name='documents'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('restore/', views.restore, name='restore'),
    # path('#/', views.#, name='#'),
]
