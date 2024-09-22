from rest_framework import serializers
from QuestionBank.api.serializers import DynamicQuestionSerializer

from Test.models import Test

class TestSerializer(serializers.ModelSerializer):
    questions = DynamicQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'topic', 'description', 'questions', 'created_by', 'created_on', 'updated_at']

class TestListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        exclude = ['questions', 'created_on', 'updated_at']