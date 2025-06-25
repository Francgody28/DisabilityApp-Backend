from django.urls import path
from . import views
from django.urls import path
from .views import register_disabled_person
from .views import LocationListCreateView
from .views import delete_location


urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('register-disabled/', register_disabled_person),
    path('register-disabled/<int:id>/', views.delete_person),
    path('location/', LocationListCreateView.as_view(), name='location-list-create'),   
    path('location/<int:pk>/', delete_location, name='delete-location'),
]
