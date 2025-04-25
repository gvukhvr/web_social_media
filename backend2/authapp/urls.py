from django.urls import path
from .views import RegisterView, LoginView, UserView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('users/', UserListView.as_view(), name='user-list'),  
]
