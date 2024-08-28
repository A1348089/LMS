from django.urls import path
from courses.views import *

urlpatterns = [

    # Field URLS
    path('',FieldList.as_view(),name="field-list-all"), # View all the fields
    path('create',FieldListCreate.as_view(),name="field-create"),
    path('<int:pk>/',FieldDetail.as_view(),name="field-details"), # Access perticular field to perform CRUD 

    # Category URLS
    path('category/',CategoryList.as_view(),name="category-list-all"), # view all the Category
    path('<int:pk>/category/',CategoryList.as_view(),name="category-list"), # view all the Category based on field id
    path('<int:pk>/category/create',CategoryCreate.as_view(),name="category-create"),  # create Category for a specified field id
    path('<int:field_pk>/category/<int:pk>/',CategoryDetail.as_view(),name="category-details"), # Access perticulal category to perform retrive, Update, and Delete for a specified field id

    # Course URLS
    path('courses/', CourseList.as_view(), name='course-list'),
    path('course/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    
    path('<int:field_pk>/category/<int:pk>/course/', CourseList.as_view(), name='course-list'),
    path('<int:field_pk>/category/<int:pk>/course/create/', CourseCreate.as_view(), name='course-create'),
    path('<int:field_pk>/category/<int:category_pk>/add_course/', ListAndAddCourseToCategory.as_view(), name='list-and-add-course-to-category'),
    path('<int:field_pk>/category/<int:category_pk>/course/<int:pk>/', CourseDetail.as_view(), name='course-detail'),

]