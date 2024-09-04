from courses.api.serializers import *

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from courses.api.permissions import AdminOrReadOnly

from django.shortcuts import get_object_or_404
# Create your views here.

# ################ Field Views Start ####################

class FieldList(generics.ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    # permission_classes = [AdminOrReadOnly]

class FieldListCreate(generics.ListCreateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    # permission_classes = [AdminOrReadOnly]

class FieldDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    # permission_classes = [AdminOrReadOnly]

################ Field Views End ####################

################ Category Views Start ####################

class CategoryList(generics.ListAPIView):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [AdminOrReadOnly]

    def get_queryset(self):
        field_id = self.kwargs.get('pk')
        if field_id:
            try:
                return Category.objects.filter(field__id=field_id)
            except ValueError:
                return Category.objects.none()
        else:
            return Category.objects.all()
    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    # permission_classes = [AdminOrReadOnly]
    def get_queryset(self):
        field_id = self.kwargs['field_pk'] # retrive field id from the url
        
        return Category.objects.filter(field_id=field_id)

class CategoryCreate(generics.CreateAPIView):
    serializer_class = CategorySerializer
    # permission_classes = [AdminOrReadOnly]
    def perform_create(self, serialiser):
        field_id = self.kwargs.get('pk')
        field = Field.objects.get(pk=field_id)
        serialiser.save(field=field)
################ Category Views End ####################

################ Course Views Start ####################

# List all course for a given Category
class CourseList(generics.ListAPIView):
    serializer_class = CourseSerializer
    # permission_classes = [AdminOrReadOnly]

    def get_queryset(self):
        category_id = self.kwargs.get('pk')  # Get category ID from URL

        if category_id:
            try:
                return Course.objects.filter(category__id=category_id)
            except ValueError:
                return Course.objects.none()  # Return an empty queryset on error
        else:
            return Course.objects.all()
        
# Create a new Course for a given Category
class CourseCreate(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    # permission_classes = [AdminOrReadOnly]
    def get_queryset(self):
        return Course.objects.all()
    
    def perform_create(self, serializer):
        category_id = self.kwargs.get('pk')  # Get category ID from URL
        category = Category.objects.get(pk=category_id)
        serializer.save(category=[category])  # ManyToMany relationship 
        return Response({
                "message": f"The Course is added for '{category.category_name}' created Successfull"
            },
            status=status.HTTP_201_CREATED)

class ListAndAddCourseToCategory(generics.ListCreateAPIView):
    serializer_class = CourseSerializer
    # permission_classes = [AdminOrReadOnly]
    def get_queryset(self):
        # List all available Course instances
        return Course.objects.all()

    def create(self, request, *args, **kwargs):
        category_pk = self.kwargs.get('category_pk')
        category = get_object_or_404(Category, pk=category_pk)

        # Retrieve the Course IDs from the request data
        course_ids = request.data.get('course_ids', [])
        if course_ids:
            courses = Course.objects.filter(id__in=course_ids)

            # Add the courses to the category
            for course in courses:
                course.category.add(category)

            return Response({
                "message": f"Courses added to Category '{category.category_name}'",
                "courses": [course.course_name for course in courses]
            },
            status=status.HTTP_201_CREATED)
        else:
            # Handle the case where no course_ids are provided
            return Response({
                "message": "No course IDs provided",
            }, status=status.HTTP_400_BAD_REQUEST)  # Bad Request

# Retrieve, Update, and Delete a specific Course
class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [AdminOrReadOnly]
    serializer_class = CourseSerializer
    def get_queryset(self):
        course_id = self.kwargs['pk']
        return Course.objects.filter(pk=course_id)
################ Course Views End ####################
