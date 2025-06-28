
from django.urls import path
from .views import (
    register_user,
    login_user,
    register_disabled_person,
    delete_person,
    update_disabled_person,
    location_list_create,
    update_location,
    delete_location
)

urlpatterns = [
    # Auth
    path('register/', register_user),
    path('login/', login_user),

    # Disabled Person
    path('register-disabled/', register_disabled_person),
    path('register-disabled/<int:id>/', delete_person),
    path('update-disabled/<int:pk>/', update_disabled_person),

    # Location
    path('location/', location_list_create),
    path('location/<int:pk>/', update_location),
    path('delete-location/<int:pk>/', delete_location),
]
