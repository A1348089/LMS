from QuestionBank.models import Question
from QuestionBank.api.serializers import DynamicQuestionSerializer

from Test.models import Test
from Test.api.serializers import (TestListCreateSerializer, TestSerializer)

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

################################## Test View Start ##############################

class TestCreateView(generics.CreateAPIView):
    serializer_class = TestListCreateSerializer
    queryset = Test.objects.all()

class TestListAllView(generics.ListAPIView):
    serializer_class = TestListCreateSerializer
    queryset = Test.objects.all()

class TestRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
################################## Test View End ##############################

class AddQuestionsToTestView(APIView):
    def get(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
        
        question_type = request.query_params.get('question_type')
        course_id = request.query_params.get('course_id')

        # Step 1: Start with all questions
        questions = Question.objects.all()

        # Step 2: Filter based on question_type and course_id if they exist in query parameters
        if question_type and course_id:
            questions = questions.filter(question_type=question_type, course_id=course_id)
        elif question_type:
            questions = questions.filter(question_type=question_type)
        elif course_id:
            questions = questions.filter(course_id=course_id)

        # Step 3: Exclude questions that are already part of the test
        questions = questions.exclude(id__in=test.questions.values_list('id', flat=True))

        # Step 4: Serialize the filtered questions to display them
        serializer = DynamicQuestionSerializer(questions, many=True)

        # If no questions are found, return an error
        if not questions.exists():
            return Response({"error": "No questions found based on the provided filters."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            "message": "List of Questions",
            "filtered_questions": serializer.data
        }, status=status.HTTP_200_OK)
        
    def post(self, request, test_id):
        # Step 1: Retrieve the Test instance
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        questions = Question.objects.all()

        serializer = DynamicQuestionSerializer(questions, many=True)
        
        # Step 2: Get the list of question IDs from the request body to be added to the Test
        question_ids = request.data.get('question_ids', [])
        if not question_ids:
            return Response({"error": "No question_ids provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 3: Validate and add filtered questions based on question_ids
        valid_questions = Question.objects.filter(id__in=question_ids)
        if not valid_questions.exists():
            return Response({"error": "No valid questions found to add to the test"}, status=status.HTTP_400_BAD_REQUEST)

        test.questions.add(*valid_questions)
        
        return Response({
            "message": "Questions added successfully to the test",
            "filtered_questions": serializer.data
        }, status=status.HTTP_200_OK)
    
class RemoveQuestionsFromTestView(APIView):

    def get(self, request, test_id):
        
        test = Test.objects.get(id=test_id)

        # Step 1: get questions that are in the test
        test_questions = test.questions.all()

        # Step 2: Serialize the filtered questions to display them
        serializer = DynamicQuestionSerializer(test_questions, many=True)

        # If no questions are found, return an error
        if not test_questions.exists():
            return Response({"error": "No questions found based on the provided filters."}, status=status.HTTP_404_NOT_FOUND)
        
        if test_questions.exists():
            return Response({
            "message": "List of Questions",
            "filtered_questions": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

        question_ids = request.data.get('question_ids', [])
        questions = Question.objects.filter(id__in=question_ids)

        if not questions.exists():
            return Response({"error": "No valid questions found"}, status=status.HTTP_400_BAD_REQUEST)

        test.questions.remove(*questions)
        return Response({"message": "Questions removed successfully"}, status=status.HTTP_200_OK)
