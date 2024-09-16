from django_filters import rest_framework as filters
from QuestionBank.models import (Question,)

class QuestionFilter(filters.FilterSet):

    class Meta:
        model = Question
        fields = ['course','question_type']