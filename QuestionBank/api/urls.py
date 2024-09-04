from django.urls import path
from QuestionBank.views import (QuestionCreateView, QuestionListView, 
                                QuestionRetrieveUpdateDestroyView, TestListCreateView,
                                AddQuestionToTestView, TestRetriveUpdateDestroyView)

urlpatterns = [
    # Questions urls Start
    path('', QuestionListView.as_view(), name="Question-list"),
    path('create/', QuestionCreateView.as_view(), name="Create-Question"),
    path('<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
    # Questions urls End

    # Test urls Start
    path('test/', TestListCreateView.as_view(), name='Test-list-create'),
    path('test/<int:pk>/', TestRetriveUpdateDestroyView.as_view(), name='Test-edit-details'),
    path('test/<int:pk>/addQuestions/', AddQuestionToTestView.as_view(), name='Test-add-questions'),
    # path('test/<int:pk>/listQuestions/', TestRetriveUpdateDestroyView.as_view(), name='Test-questions-list'),
    # Test urls End
]
