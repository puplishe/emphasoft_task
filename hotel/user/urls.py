from django.urls import path

from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='token_obtain_pair'),
]
