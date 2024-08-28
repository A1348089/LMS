from django.shortcuts import render

from rest_framework import generics

from accounts.api.serializers import CreateCustomUserSerializer
# Create your views here.

class CreateCustomUserView(generics.CreateAPIView):
    serializer_class = CreateCustomUserSerializer