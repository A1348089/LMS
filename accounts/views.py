from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status

from accounts.api.serializers import UserLoginSerializer, UserRegistrationSerializer

from rest_framework.decorators import api_view

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Create your views here.

# class RegisterUserView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     queryset = CustomUser.objects.all()

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.save()
#             if user.is_mentor:
#                 return Response({"message": "Mentor registered, pending approval by admin."}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response({"message": "Intern registered successfully."}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login_view(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Check if the user is a mentor and approved
            if user.is_mentor and not user.user_status:
                raise Response({"message": "Your approval is pending by the admin."}, status=status.HTTP_403_FORBIDDEN)

            # Generate token for the user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "token": token.key,
                "user_id": user.id
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user.is_mentor:
                return Response({"message": "Mentor registered, pending approval by admin.",
                                 "data": serializer.data},
                                 status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Intern registered successfully."}, 
                                status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, 
                            status=status.HTTP_400_BAD_REQUEST)
        
