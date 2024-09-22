from rest_framework import serializers
from Batches.models import Batches

from django.core.exceptions import PermissionDenied

from accounts.models import CustomUser
from accounts.api.serializers import CustomUserSerializer

class BatchSerializer(serializers.ModelSerializer):
    mentors = CustomUserSerializer(many=True, read_only=True)
    interns = CustomUserSerializer(many=True, read_only=True)
    pending_requests = CustomUserSerializer(many=True, read_only=True)
    created_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Batches
        fields = ['id', 'batch_name', 'created_by', 'mentors', 'interns', 'pending_requests']

    def update(self, instance, validated_data):
        request = self.context['request']
        mentors = request.data.get('mentors', [])
        interns = request.data.get('interns', [])

        # Only allow created_by to update and delete
        if request.user != instance.created_by:
            raise PermissionDenied("Only the creator can update or delete this batch.")

        # Update mentors and interns
        instance.mentors.set(CustomUser.objects.filter(id__in=mentors, is_mentor=True))
        instance.interns.set(CustomUser.objects.filter(id__in=interns, is_intern=True))
        instance.save()
        return instance
