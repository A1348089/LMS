from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from QuestionBank.api.serializers import (DynamicQuestionSerializer, QuestionSerializer)
from QuestionBank.models import (Question, FillInTheBlankQuestion,
                                 MultipleChoiceQuestion, MatchTheFollowingQuestion,
                                 TrueOrFalseQuestion)
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
# class QuestionCreateView(generics.CreateAPIView):
#     serializer_class = DynamicQuestionSerializer
#     queryset = Question.objects.all()
    
#     def perform_create(self, serializer):
#         question_data = serializer.validated_data.get('question')
#         question_type = question_data['question_type']
        
#         # Verify the question type
#         if question_type not in [Question.FILL_IN_THE_BLANK, Question.MULTIPLE_CHOICE, 
#                                  Question.MATCH_THE_FOLLOWING, Question.MULTIPLE_ANSWERS,
#                                  Question.TRUE_OR_FALSE]:
#             raise serializer.ValidationError("Invalid question type")
        
#         # Once verified, create or get the question
#         question, created = Question.objects.get_or_create(**question_data)

#         if question_type == Question.FILL_IN_THE_BLANK:
#             fill_in_the_blank_data = serializer.validated_data.get('fill_in_the_blank_question')
            
#             FillInTheBlankQuestion.objects.create(question=question, **fill_in_the_blank_data)

#         elif question_type == Question.MULTIPLE_CHOICE:
#             multiple_choice_data = serializer.validated_data.get('multiple_choice_question')
            
#             MultipleChoiceQuestion.objects.create(question=question, **multiple_choice_data)

#         elif question_type == Question.MATCH_THE_FOLLOWING:
#             match_the_following_data = serializer.validated_data.get('match_the_following_question')
            
#             MatchTheFollowingQuestion.objects.create(question=question, **match_the_following_data)

#         elif question_type == Question.MULTIPLE_ANSWERS:
#             multiple_answer_data = serializer.validated_data.get('multiple_answer_question')
            
#             MultipleChoiceQuestion.objects.create(question=question, **multiple_answer_data)

#         elif question_type == Question.TRUE_OR_FALSE:
#             true_or_false_data = serializer.validated_data.get('true_or_false_question')
            
#             TrueOrFalseQuestion.objects.create(question=question, **true_or_false_data)
#         else:
#             return Response({'status':'Select Valid Question Type'}, status=status.HTTP_400_BAD_REQUEST)
        
#         # The question and its related details are only saved after verification
#         serializer.save(question=question)
        
#         return Response({'status': 'question created'}, status=status.HTTP_201_CREATED)

################################## Create Question View End ##############################

################################## List Question View Start ##############################
# class QuestionListView(generics.ListAPIView):
#     serializer_class = DynamicQuestionSerializer

#     def get_queryset(self):
#         return Question.objects.all()