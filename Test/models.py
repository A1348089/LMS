from django.db import models

from QuestionBank.models import Question
from accounts.models import CustomUser

# Create your models here.


class Test(models.Model):
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=100, default="Topic")
    description = models.CharField(max_length=500, default="description")
    questions = models.ManyToManyField(Question, related_name='tests')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title},' ',{self.topic},' ',{self.created_on}"