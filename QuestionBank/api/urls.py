from django.urls import path
from QuestionBank.views import (QuestionCreateView, QuestionListView, 
                                QuestionRetrieveUpdateDestroyView)

urlpatterns = [
    # Questions urls Start
    path('list/', QuestionListView.as_view(), name="Questions-list"),
    path('create/', QuestionCreateView.as_view(), name="Create-Question"),
    path('<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),

]
