from rest_framework import serializers

from courses.models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        # fields = '__all__'
        exclude = ('category',)

class CategorySerializer(serializers.ModelSerializer):
    # Course = CourseSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ('field',)

class FieldSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = Field
        fields = '__all__'