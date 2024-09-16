from django.urls import path, include

from accounts.views import registration_view, user_login_view
# from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("login/", user_login_view, name='login'),
    path('register/', registration_view, name='register-user'),
]
