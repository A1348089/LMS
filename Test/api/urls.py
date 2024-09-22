from django.urls import path
from Test.views import (TestCreateView, TestListAllView, 
                        TestRetrieveUpdateDestroyView, AddQuestionsToTestView, 
                        RemoveQuestionsFromTestView)

urlpatterns = [
    # Test urls Start
    path('create/', TestCreateView.as_view(), name='Test-create'),
    path('list/', TestListAllView.as_view(), name='Test-list-all'),
    path('<int:pk>/', TestRetrieveUpdateDestroyView.as_view(), name='Test-edit-details'),
    path('<int:test_id>/add-questions/', AddQuestionsToTestView.as_view(), name='add-questions-to-test'),
    path('<int:test_id>/remove-questions/', RemoveQuestionsFromTestView.as_view(), name='remove-questions-from-test'),

]