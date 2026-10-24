from django.urls import path
from . import views, api

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_list, name='list'),
    path('my-profile/', views.doctor_edit, name='edit'),
    path('availability/', views.availability, name='availability'),
    path('availability/<int:pk>/delete/', views.availability_delete, name='availability_delete'),
    path('schedule/', views.schedule_live, name='schedule_live'),
    path('api/availability/', api.availability_list, name='api_availability'),
    path('api/availability/add/', api.availability_add, name='api_availability_add'),
    path('api/availability/<int:pk>/update/', api.availability_update, name='api_availability_update'),
    path('api/availability/<int:pk>/delete/', api.availability_delete_api, name='api_availability_delete'),
    path('map/', views.doctor_map, name='map'),
    path('<int:pk>/', views.doctor_detail, name='detail'),
]