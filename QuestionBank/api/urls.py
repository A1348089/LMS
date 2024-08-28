from django.urls import path
from QuestionBank.views import (QuestionCreateView,QuestionListView, QuestionRetrieveUpdateDestroyView)

urlpatterns = [
    path('', QuestionListView.as_view(), name="Question-list"),
    path('create/', QuestionCreateView.as_view(), name="Create-Question"),
    path('<int:id>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
]
