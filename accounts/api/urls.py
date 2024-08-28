from django.urls import path

from accounts.views import CreateCustomUserView

urlpatterns = [
    path('register/',CreateCustomUserView.as_view(), name='create-user'),
]
