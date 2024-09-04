from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from QuestionBank.api.serializers import (DynamicQuestionSerializer, QuestionSerializer,
                                          TestListCreateSerializer, TestRetrieveSerializer,
                                          TestQuestionAddSerializer)
from QuestionBank.models import (Question, FillInTheBlankQuestion,
                                 MultipleChoiceQuestion, MatchTheFollowingQuestion,
                                 TrueOrFalseQuestion, Test)
from courses.models import Course

################################## Create Question View Start ##############################

class QuestionCreateView(generics.CreateAPIView):
    serializer_class = DynamicQuestionSerializer
    queryset = Question.objects.all()
    
    def perform_create(self, serializer):
        # Validate and verify the question type
        question_type = serializer.validated_data.get('question_type')
        
        if question_type not in [Question.FILL_IN_THE_BLANK, Question.MULTIPLE_CHOICE, 
                                 Question.MATCH_THE_FOLLOWING, Question.MULTIPLE_ANSWERS,
                                 Question.TRUE_OR_FALSE]:
            raise serializer.ValidationError("Invalid question type")

        # Create the question and associated nested objects
        question = serializer.save()

        return Response({'status': 'Question created'}, status=status.HTTP_201_CREATED)
    
################################## Create Question View End ##############################

################################## List Question View Start ##############################

class QuestionListView(generics.ListAPIView):
    serializer_class = DynamicQuestionSerializer
    queryset = Question.objects.all()
    
    def get_queryset(self):
        """
        Optionally restricts the returned questions,
        by filtering against query parameters in the URL.
        """
        queryset = super().get_queryset()
        question_type = self.request.query_params.get('question_type')
        
        if question_type == Question.FILL_IN_THE_BLANK:
            queryset = queryset.filter(fillintheblankquestion__isnull=False)
        elif question_type == Question.MULTIPLE_CHOICE:
            queryset = queryset.filter(multiplechoicequestion__isnull=False)
        elif question_type == Question.MATCH_THE_FOLLOWING:
            queryset = queryset.filter(matchthefollowingquestion__isnull=False)
        elif question_type == Question.MULTIPLE_ANSWERS:
            queryset = queryset.filter(multiplechoicequestion__isnull=False)
        elif question_type == Question.TRUE_OR_FALSE:
            queryset = queryset.filter(trueorfalsequestion__isnull=False)
        
        return queryset
    
################################## List Question View End ################################

################################## RetrieveUpdateDestroy Question View Start ##############################

class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DynamicQuestionSerializer
    queryset = Question.objects.all()
    lookup_field = 'id'  # Assuming 'id' is the primary key

    def perform_update(self, serializer):
        # This will save the updated Question object and its related data
        serializer.save()

    def perform_destroy(self, instance):
        # Custom delete logic if necessary
        instance.delete()

    def get_queryset(self):
        """
        Optionally restricts the returned questions,
        by filtering against query parameters in the URL.
        """
        queryset = super().get_queryset()
        question_type = self.request.query_params.get('question_type')
        
        if question_type:
            queryset = queryset.filter(question_type=question_type)
        
        return queryset
    
################################## RetrieveUpdateDestroy Question View End ##############################

################################## Test View Start ##############################

class TestListCreateView(generics.ListCreateAPIView):
    serializer_class = TestListCreateSerializer
    queryset = Test.objects.all()
################################## Test View End ##############################
from django_filters.rest_framework import DjangoFilterBackend

class AddQuestionToTestView(generics.ListCreateAPIView, QuestionListView):
    serializer_class = DynamicQuestionSerializer
    queryset = Question.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'question_type']

    def get_queryset(self):
        return QuestionListView.get_queryset(self)
    
    def post(self, request, *args, **kwargs):
        test_id = self.kwargs.get('pk')
        test_obj = get_object_or_404(Test, id=test_id)

        questions_ids = request.data.get('questions_ids', [])
        if questions_ids:
            questions = Question.objects.filter(id__in=questions_ids)

            # Add the Questions to the Test
            for question in questions:
                question.test.add(test_obj)

            return Response({
                "message": f"Questions added to the Test '{test_obj.title}'",
                "Questions": [question.question_text for question in questions]
            }, status=status.HTTP_201_CREATED)
        
        elif request.data:  # Check if there is data to serialize
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                # Save the new question
                question = serializer.save()

                # Map the new question to the test
                question.test.add(test_obj)

                return Response({
                    "message": f"Question '{question.question_text}' created and added to the Test '{test_obj.title}'",
                    "Question": question.question_text
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "message": "No Questions were Added"
        }, status=status.HTTP_400_BAD_REQUEST)
    
    
    # def update_or_create(self, request, serializer, *args, **kwargs):

    #     test_id = self.kwargs.get('pk')
    #     test_obj = get_object_or_404(Test, id=test_id)

    #     questions_ids = request.data.get('questions_ids',[])
    #     if questions_ids:
    #         questions = Question.objects.filter(id__in = questions_ids)

    #         # Add the Questions to the Test
    #         for question in questions:
    #             question.test.add(test_obj)
    #         return Response({
    #             "message":f"Questions added to the Test '{test_obj.title}'","Questions": [question.question_text for question in questions]},
    #             status=status.HTTP_201_CREATED)
        
    #     elif serializer.validated_data:

    #     else:
    #         return Response({
    #             "message":"No Questions are Added"
    #         },
    #         status=status.HTTP_400_BAD_REQUEST)
        

# class AddQuestionToTestView(generics.ListCreateAPIView, QuestionListView):
#     serializer_class = TestRetrieveSerializer
#     def get_queryset(self):
#         test_id = self.kwargs.get('pk')
#         return Test.objects.filter(id=test_id)
    
#     def create(self, request, *args, **kwargs):
#         test_id = self.kwargs.get('pk')
#         test_obj = get_object_or_404(Test, id=test_id)

#         questions_ids = request.data.get('questions_ids',[])
#         if questions_ids:
#             questions = Question.objects.filter(id__in = questions_ids)

#             # Add the Questions to the Test
#             for question in questions:
#                 question.test.add(test_obj)
#             return Response({
#                 "message":f"Questions added to the Test '{test_obj.title}'","Questions": [question.question_text for question in questions]},
#                 status=status.HTTP_201_CREATED)
#         else:
#             return Response({
#                 "message":"No Questions are Added"
#             },
#             status=status.HTTP_400_BAD_REQUEST)
        
class TestRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestRetrieveSerializer
    
    queryset = Test.objects.all()