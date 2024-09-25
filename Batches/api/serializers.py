from Batches.models import Batches, BatchInternRelation

from accounts.models import CustomUser
from accounts.api.serializers import CustomUserSerializer

from rest_framework import serializers

class BatchInternRelationSerializer(serializers.ModelSerializer):
    intern_username = serializers.CharField(source='intern.username', read_only=True)
    batch_name = serializers.CharField(source='batch.batch_name', read_only=True)

    class Meta:
        model = BatchInternRelation
        fields = ['intern', 'batch', 'status', 'intern_username', 'batch_name']
        read_only_fields = ['intern_username', 'batch_name']


class BatchSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    mentors = CustomUserSerializer(many=True, read_only=True)
    interns = CustomUserSerializer(many=True, read_only=True)
    pending_requests = serializers.SerializerMethodField()

    class Meta:
        model = Batches
        fields = ['id', 'batch_name', 'status', 'created_by', 'mentors', 'interns', 'pending_requests']

    def get_pending_requests(self, obj):
        pending_interns = BatchInternRelation.objects.filter(batch=obj, status=BatchInternRelation.PENDING)
        return BatchInternRelationSerializer(pending_interns, many=True).data

class BatchRequestSerializer(serializers.Serializer):
    intern_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(is_intern=True))
    action = serializers.ChoiceField(choices=['approve', 'reject', 'request'])

    def validate(self, data):
        intern = data.get('intern_id')
        batch = self.context['batch']
        
        # Ensure the intern has not already been approved/rejected
        if BatchInternRelation.objects.filter(intern=intern, batch=batch).exclude(status=BatchInternRelation.PENDING).exists():
            raise serializers.ValidationError('This intern has already exists in this batch')
        
        return data

    def save(self, **kwargs):
        action = self.validated_data.get('action')
        intern = self.validated_data.get('intern_id')
        batch = self.context['batch']

        if action == 'approve':
            batch.approve_intern(intern)
        elif action == 'reject':
            batch.reject_intern(intern)
        elif action == 'request':
            BatchInternRelation.objects.create(intern=intern, batch=batch, status=BatchInternRelation.PENDING)