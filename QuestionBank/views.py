
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from QuestionBank.api.serializers import DynamicQuestionSerializer
from QuestionBank.models import Question

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