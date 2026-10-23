from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='list'),
    path('map/', views.doctor_map, name='map'),
    path('<int:pk>/', views.doctor_detail, name='detail'),
    path('my-profile/', views.doctor_edit, name='edit'),
    path('availability/', views.availability, name='availability'),
    path('availability/<int:pk>/delete/', views.availability_delete, name='availability_delete'),
]