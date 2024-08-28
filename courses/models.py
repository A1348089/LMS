from django.db import models

# Create your models here.


class Field(models.Model):
    field_name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.field_name
    
class Category(models.Model):
    category_name = models.CharField(max_length=100, null=False)
    field = models.ForeignKey(Field, on_delete=models.CASCADE,related_name="category")
    def __str__(self):
        return self.category_name
    
class Course(models.Model):
    course_name = models.CharField(max_length=100, null=False)
    category = models.ManyToManyField(Category,related_name="course")

    def __str__(self):
        return self.course_name