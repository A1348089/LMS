from django.urls import path
from Test.views import (TestCreateView, TestListAllView, TestRetrieveUpdateDestroyView)

urlpatterns = [
    # Test urls Start
    path('create/', TestCreateView.as_view(), name='Test-create'),
    path('', TestListAllView.as_view(), name='Test-list-all'),
    path('<int:pk>/', TestRetrieveUpdateDestroyView.as_view(), name='Test-edit-details'),

]


