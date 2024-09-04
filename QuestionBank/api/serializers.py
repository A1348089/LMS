from rest_framework import serializers
from accounts.models import CustomUser
from QuestionBank.models import (FillInTheBlankQuestion, MatchTheFollowingQuestion, 
                                 MultipleChoiceQuestion, TrueOrFalseQuestion, 
                                 Question, Test, Attempt)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'course', 'question_text', 'question_type', 'description', 'marks', 'created_by', 'is_public']

class FillInTheBlankQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FillInTheBlankQuestion
        fields = ['answer']

class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['choices', 'correct_answers']

class MatchTheFollowingQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchTheFollowingQuestion
        fields = ['pairs']

class MultipleAnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleChoiceQuestion
        fields = ['choices', 'correct_answers']

class TrueOrFalseQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrueOrFalseQuestion
        fields = ['correct_answer']
        
class DynamicQuestionSerializer(serializers.ModelSerializer):
    
    fill_in_the_blank_question = FillInTheBlankQuestionSerializer(required=False)
    multiple_choice_question = MultipleChoiceQuestionSerializer(required=False)
    match_the_following_question = MatchTheFollowingQuestionSerializer(required=False)
    multiple_answer_question = MultipleAnswerQuestionSerializer(required=False)
    true_or_false_question = TrueOrFalseQuestionSerializer(required=False)

    class Meta:
        model = Question
        fields = '__all__'
    
    def create(self, validated_data):
        # Extract the nested data for related models
        fill_in_the_blank_data = validated_data.pop('fill_in_the_blank_question', None)
        multiple_choice_data = validated_data.pop('multiple_choice_question', None)
        match_the_following_data = validated_data.pop('match_the_following_question', None)
        multiple_answer_data = validated_data.pop('multiple_answer_question', None)
        true_or_false_data = validated_data.pop('true_or_false_question', None)
        # Create the Question object
        question = Question.objects.create(**validated_data)
        
        # Based on the question type, create the related objects
        if fill_in_the_blank_data:
            FillInTheBlankQuestion.objects.create(question=question, **fill_in_the_blank_data)

        elif multiple_choice_data:
            MultipleChoiceQuestion.objects.create(question=question, **multiple_choice_data)

        elif match_the_following_data:
            MatchTheFollowingQuestion.objects.create(question=question, **match_the_following_data)

        elif match_the_following_data:
            MatchTheFollowingQuestion.objects.create(question=question, **match_the_following_data)

        elif multiple_answer_data:
            MultipleChoiceQuestion.objects.create(question=question, **multiple_answer_data)

        elif true_or_false_data:
            TrueOrFalseQuestion.objects.create(question=question, **true_or_false_data)

        return question
    
    def update(self, instance, validated_data):
        fill_in_the_blank_data = validated_data.pop('fill_in_the_blank_question', None)
        multiple_choice_data = validated_data.pop('multiple_choice_question', None)
        match_the_following_data = validated_data.pop('match_the_following_question', None)
        multiple_answer_data = validated_data.pop('multiple_answer_question', None)
        true_or_false_data = validated_data.pop('true_or_false_question', None)
        
        # Update the Question object
        instance = super().update(instance, validated_data)
        
        # Update or create the related objects based on question type
        if fill_in_the_blank_data:
            fill_in_the_blank_question, created = FillInTheBlankQuestion.objects.update_or_create(
                question=instance, defaults=fill_in_the_blank_data
            )
        elif multiple_choice_data:
            multiple_choice_question, created = MultipleChoiceQuestion.objects.update_or_create(
                question=instance, defaults=multiple_choice_data
            )
        elif match_the_following_data:
            match_the_following_question, created = MatchTheFollowingQuestion.objects.update_or_create(
                question=instance, defaults=match_the_following_data
            )
        elif multiple_answer_data:
            multiple_answer_question, created = MatchTheFollowingQuestion.objects.update_or_create(
                question=instance, defaults=multiple_answer_data
            )
        elif true_or_false_data:
            true_or_false_question, created = TrueOrFalseQuestion.objects.update_or_create(
                question=instance, defaults=true_or_false_data
            )
        
        return instance
    
    def to_representation(self, instance):
        # Start with the default representation
        ret = super().to_representation(instance)

        # Add related data based on question type
        try:
            if instance.question_type == Question.FILL_IN_THE_BLANK:
                if FillInTheBlankQuestion.objects.filter(question=instance).exists():
                    fill_in_the_blank_question = FillInTheBlankQuestion.objects.get(question=instance)
                    ret['fill_in_the_blank_question'] = FillInTheBlankQuestionSerializer(fill_in_the_blank_question).data
                else:
                    ret['fill_in_the_blank_question'] = None

            elif instance.question_type in [Question.MULTIPLE_CHOICE, Question.MULTIPLE_ANSWERS]:
                if MultipleChoiceQuestion.objects.filter(question=instance).exists():
                    multiple_choice_question = MultipleChoiceQuestion.objects.get(question=instance)
                    ret['multiple_choice_question'] = MultipleChoiceQuestionSerializer(multiple_choice_question).data
                else:
                    ret['multiple_choice_question'] = None

            elif instance.question_type == Question.MATCH_THE_FOLLOWING:
                if MatchTheFollowingQuestion.objects.filter(question=instance).exists():
                    match_the_following_question = MatchTheFollowingQuestion.objects.get(question=instance)
                    ret['match_the_following_question'] = MatchTheFollowingQuestionSerializer(match_the_following_question).data
                else:
                    ret['match_the_following_question'] = None

            elif instance.question_type == Question.TRUE_OR_FALSE:
                if TrueOrFalseQuestion.objects.filter(question=instance).exists():
                    true_or_false_question = TrueOrFalseQuestion.objects.get(question=instance)
                    ret['true_or_false_question'] = TrueOrFalseQuestionSerializer(true_or_false_question).data
                else:
                    ret['true_or_false_question'] = None

        except MultipleChoiceQuestion.DoesNotExist:
            ret = None

        return ret

class TestListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Test
        # fields = '__all__'
        exclude = ('description', 'questions', 'created_on', 'updated_at',)

class TestRetrieveSerializer(serializers.ModelSerializer):
    questions = DynamicQuestionSerializer(many=True, required=False, read_only = True)
    class Meta:
        model = Test
        fields = '__all__'

class TestQuestionAddSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Test
        # fields = '__all__'
        exclude = ('questions','created_on','updated_at')