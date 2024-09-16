from django.shortcuts import get_object_or_404, render

from QuestionBank.models import Question
from QuestionBank.views import QuestionListView
from QuestionBank.api.serializers import DynamicQuestionSerializer

from Test.models import Test
from Test.api.serializers import (TestCreateSerializer, TestListAllSerializer, TestRetrieveSerializer)

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

################################## Test View Start ##############################

class TestCreateView(generics.CreateAPIView):
    serializer_class = TestCreateSerializer
    queryset = Test.objects.all()
################################## Test View End ##############################
# from django_filters.rest_framework import DjangoFilterBackend

# class AddQuestionToTestView(generics.ListCreateAPIView, QuestionListView):
#     serializer_class = DynamicQuestionSerializer
#     queryset = Question.objects.all()
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['course', 'question_type']

#     def get_queryset(self):
#         return QuestionListView.get_queryset(self)
    
#     def post(self, request, *args, **kwargs):
#         test_id = self.kwargs.get('pk')
#         test_obj = get_object_or_404(Test, id=test_id)

#         questions_ids = request.data.get('questions_ids', [])
#         action = request.data.get('action')
#         if questions_ids and action:
#             questions = Question.objects.filter(id__in=questions_ids)

#             # Add the Questions to the Test
#             for question in questions:
#                 if action == "add":
#                     question.test.add(test_obj)

#                     return Response(
#                         {
#                             "message": f"Questions added to the Test '{test_obj.title}'",
#                             "Questions": [question.question_text for question in questions]
#                             },
#                             status=status.HTTP_201_CREATED)
#                 elif action == "remove":
#                     question.test.remove(test_obj)
#                     return Response(
#                         {
#                             "message": f"Questions removed from the Test '{test_obj.title}'",
#                             "Questions": [question.question_text for question in questions]
#                             },
#                             status=status.HTTP_201_CREATED)
#                 else:
#                     return Response(
#                         {
#                             "error": "invalid action"
#                             },
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         elif request.data:  # Check if there is data to serialize
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 # Save the new question
#                 question = serializer.save()
#                 # Map the new question to the test
#                 question.test.add(test_obj)

#                 return Response({
#                     "message": f"Question '{question.question_text}' created and added to the Test '{test_obj.title}'",
#                     "Question": question.question_text
#                 }, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(
#             {
#             "message": "No Questions were Added"
#         }, 
#         status=status.HTTP_400_BAD_REQUEST)

class TestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRetrieveSerializer
    queryset = Test.objects.all()

class TestListAllView(generics.ListAPIView):
    serializer_class = TestListAllSerializer
    queryset = Test.objects.all()
