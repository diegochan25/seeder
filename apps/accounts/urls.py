from django.urls import path
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.sign_in, name='sign_in'),
    path('password/forgot', views.forgot_password, name='forgot_password'),
    path('password/reset', views.reset_password, name='reset_password')
]
