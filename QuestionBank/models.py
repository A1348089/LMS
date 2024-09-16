from django.db import models
import Test
from accounts.models import CustomUser
from courses.models import Course
# Create your models here.
class Question(models.Model):
    FILL_IN_THE_BLANK = "FIBL"
    MULTIPLE_CHOICE = "MCQ"
    MATCH_THE_FOLLOWING = "MTF"
    MULTIPLE_ANSWERS = "MAMCQ"
    TRUE_OR_FALSE = "TF"

    QUESTION_TYPE_CHOICES = [
        (FILL_IN_THE_BLANK, "Fill in the Blank"),
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (MATCH_THE_FOLLOWING, "Match the Following"),
        (MULTIPLE_ANSWERS, "Multiple Answered Question"),
        (TRUE_OR_FALSE, "True or False"),
    ]

    course = models.ForeignKey(Course, default=None, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES, default=FILL_IN_THE_BLANK)
    description = models.CharField(max_length=250)
    marks = models.FloatField(default=1)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.question_text

class FillInTheBlankQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    answer = models.CharField(max_length=255)

class MultipleChoiceQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    choices = models.JSONField()  # Example: {"A": "Option 1", "B": "Option 2"}
    correct_answers = models.JSONField()  # Example: ["A", "C"]

    def check_answer(self, given_answers):
        return set(given_answers) == set(self.correct_answers)

class MatchTheFollowingQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    pairs = models.JSONField()  # Example: {"A": "1", "B": "2"}

class TrueOrFalseQuestion(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)
    correct_answer = models.BooleanField()  # True or False

    def check_answer(self, given_answer):
        return given_answer == self.correct_answer
    
class Attempt(models.Model):
    intern = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.JSONField()  # Store intern's answers
    score = models.FloatField(null=True, blank=True)  # Calculated after submission
    completed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intern.first_name},' ',{self.test.title},' ',{self.score}"