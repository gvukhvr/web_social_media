# profileapp/urls.py
from django.urls import path
from .views import ProfileView
from .views import get_profile, create_profile, update_profile, delete_profile, list_users

urlpatterns = [
    path('', ProfileView.as_view(), name='profile'),
    path('profile/', get_profile, name='get-profile'),
    path('profile/create/', create_profile, name='create-profile'),
    path('profile/update/', update_profile, name='update-profile'),
    path('profile/delete/', delete_profile, name='delete-profile'),
    path('users/', list_users, name='list-users'),
]
