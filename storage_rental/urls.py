from django.urls import path
from storage_rental import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('tariffs/', views.tariffs, name='tariffs'),
    path('calculator/', views.calculator, name='calculator'),
    path('rent_box/', views.rent_box, name='rent_box'),
    path('faq/', views.faq, name='faq'),
    path('locations/', views.locations, name='locations'),
    path('contacts/', views.contacts, name='contacts'),
    path('customers_reviews/', views.customers_reviews, name='customers_reviews'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('documents/', views.documents, name='documents'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_out/', views.sign_out, name='sign_out'),
    path('restore/', views.restore, name='restore'),
    path('account/', views.account, name='account'),
    path('change_user_info/', views.change_user_info, name='change_user_info'),
    path('notifications/', views.notifications, name='notifications'),
    path('payment', views.payment, name='payment'),
    path('pay_result', views.pay_result, name='pay_result'),
]
