from rest_framework import serializers
from QuestionBank.api.serializers import DynamicQuestionSerializer

from Test.models import Test

class TestSerializer(serializers.ModelSerializer):
    questions = DynamicQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'topic', 'description', 'duration', 'questions', 'created_by', 'created_on', 'updated_at']
        extra_kwargs={
            'created_on':{'read_only':True},
            'updated_at':{'read_only':True}
        }

class TestListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        exclude = ['questions', 'created_on', 'updated_at']