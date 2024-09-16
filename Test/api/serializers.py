from rest_framework import serializers
from QuestionBank.api.serializers import DynamicQuestionSerializer
from QuestionBank.models import Question

from Test.models import Test
from Test.api.questions_filters import QuestionFilter



class TestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['title', 'questions', 'description', 'created_by']

class TestListAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        fields = ['title', 'topic', 'description', 'created_by', 'questions']

class TestRetrieveSerializer(serializers.ModelSerializer):
    question_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Test
        fields = ['title', 'topic', 'description', 'created_by', 'questions', 'question_list']

    def get_question_list(self, test):
        # Get all questions associated with the test
        questions = test.questions.all()

        # Get the request from the context to apply filtering
        request = self.context.get('request')

        # Apply filtering if there are query parameters
        if request.GET:
            questions = Question.objects.all()
            filtered_questions = QuestionFilter(request.GET, queryset=questions).qs
        else:
            filtered_questions = questions

        # If no questions match, return an empty list
        if not filtered_questions.exists():
            return []

        # Serialize the filtered questions using DynamicQuestionSerializer
        question_data = DynamicQuestionSerializer(filtered_questions, many=True).data
        
        return question_data