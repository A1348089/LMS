from django.contrib.auth import authenticate
from rest_framework import serializers
from accounts.models import CustomUser

from datetime import datetime

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'password2', 'is_mentor', 'is_intern']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    # def create(self, validated_data):
    #     email = validated_data['email']
    #     is_mentor = validated_data.get('is_mentor', False)
    #     is_intern = validated_data.get('is_intern', False)

    #     # Generate username based on role
    #     if is_mentor:
    #         username = self.generate_username(prefix="AGM", is_mentor=True)
    #     elif is_intern:
    #         username = self.generate_username(prefix="AGI", is_intern=True)
    #     else:
    #         username = None  # Handle case when neither is_mentor nor is_intern

    #     user = CustomUser.objects.create(
    #         email=email,
    #         is_mentor=is_mentor,
    #         is_intern=is_intern,
    #         username=username
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def save(self):
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        is_mentor = self.validated_data.get('is_mentor', False)
        is_intern = self.validated_data.get('is_intern', False)

        # Ensure only one of is_mentor or is_intern is True
        if is_mentor and is_intern:
            raise serializers.ValidationError("A user cannot be both mentor and intern.")
        elif not is_mentor and not is_intern:
            raise serializers.ValidationError("A user must be either a mentor or an intern.")

        # Generate username based on role
        if is_mentor:
            username = self.generate_username(prefix="AGM", is_mentor=True)
        else:
            username = self.generate_username(prefix="AGI", is_intern=True)

        # Confirming the password
        if password != password2:
            raise serializers.ValidationError({'error': 'Password and confirm password must be the same'})

        # Handling email duplicates
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'User with this email already exists'})

        # Creating the user
        user = CustomUser.objects.create(
            username=username,
            email=email,
            is_intern=is_intern,
            is_mentor=is_mentor
        )
        user.set_password(password)
        user.save()

        return user
    
    def generate_username(self, prefix, is_mentor=False, is_intern=False):
        current_year = datetime.now().year
        current_month = f"{datetime.now().month:02}"  # Format month as 2 digits
        year_month = f"{current_year}{current_month}"

        # Filter based on the role and count existing users with matching username pattern
        if is_mentor:
            count = CustomUser.objects.filter(
                username__startswith=f"{prefix}{year_month}",
                is_mentor=True,
                is_intern=False
            ).count()
        elif is_intern:
            count = CustomUser.objects.filter(
                username__startswith=f"{prefix}{year_month}",
                is_intern=True,
                is_mentor=False
            ).count()
        else:
            count = 0

        # Generate username with prefix, year_month, and count
        new_username = f"{prefix}{year_month}{count + 1}"
        return new_username

class UserLoginSerializer(serializers.ModelSerializer):
    dynamic_input = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['dynamic_input', 'password']

    def validate(self, data):
        """
        Custom validate method to ensure the user can be authenticated.
        Also checks if the user is a mentor and whether they are approved.
        """
        dynamic_input = data.get('dynamic_input')
        password = data.get('password')

        # Try to authenticate the user based on username or email
        if '@' in dynamic_input:
            user = CustomUser.objects.filter(email=dynamic_input).first()
        else:
            user = CustomUser.objects.filter(username=dynamic_input).first()

        if user is None:
            raise serializers.ValidationError("User not found with the given credentials.")

        # Use Django's authenticate method to verify the password
        user = authenticate(username=user.username, password=password)

        if user is None:
            raise serializers.ValidationError("Incorrect password.")

        # Check mentor approval status
        if user.is_mentor and not user.user_status:
            raise serializers.ValidationError("Your approval is pending by the admin.")

        data['user'] = user
        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_mentor', 'is_intern']