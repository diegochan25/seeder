from django.urls import path
from apps.schemas import views

app_name = 'schemas'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/', views.show, name='show'),
    path('new/', views.index, name='new'),
    path('', views.index, name='index'),
    path('', views.index, name='index'),
]
