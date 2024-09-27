from Batches.models import Batches, BatchInternRelation

from accounts.models import CustomUser
from accounts.api.serializers import CustomUserSerializer

from rest_framework import serializers

class BatchInternRelationSerializer(serializers.ModelSerializer):
    intern_email = serializers.CharField(source='intern.email', read_only=True)
    intern_username = serializers.CharField(source='intern.username', read_only=True)
    batch_name = serializers.CharField(source='batch.batch_name', read_only=True)

    class Meta:
        model = BatchInternRelation
        fields = ['intern', 'batch', 'status', 'intern_email', 'intern_username', 'batch_name']


class BatchSerializer(serializers.ModelSerializer):
    created_by = CustomUserSerializer(read_only=True)
    mentors = CustomUserSerializer(many=True, read_only=True)
    interns = serializers.SerializerMethodField()
    pending_requests = serializers.SerializerMethodField()
    interns_rejected = serializers.SerializerMethodField()

    class Meta:
        model = Batches
        fields = ['id', 'batch_name', 'status', 'created_by', 'mentors', 'interns', 'pending_requests', 'interns_rejected']

    def get_pending_requests(self, obj):
        pending_interns = BatchInternRelation.objects.filter(batch=obj, status=BatchInternRelation.PENDING)
        return BatchInternRelationSerializer(pending_interns, many=True).data
    def get_interns(self, obj):
        interns = BatchInternRelation.objects.filter(batch=obj, status=BatchInternRelation.APPROVED)
        return BatchInternRelationSerializer(interns, many=True).data
    def get_interns_rejected(self, obj):
        interns_rejected = BatchInternRelation.objects.filter(batch=obj, status=BatchInternRelation.REJECTED)
        return BatchInternRelationSerializer(interns_rejected, many=True).data
    
# class BatchRequestSerializer(serializers.Serializer):
#     intern_email = serializers.EmailField(source='intern.email')
#     action = serializers.ChoiceField(choices=['approve', 'reject', 'request','add','remove'])

#     def validate(self, data):
#         intern = data.get('intern_id')
#         # intern_email = data.get('intern_email')
#         batch = self.context['batch']
        
#         # Ensure the intern has not already been approved/rejected
#         if BatchInternRelation.objects.filter(intern=intern, batch=batch).exclude(status=BatchInternRelation.PENDING).exists():
#             raise serializers.ValidationError('This intern has already exists in this batch')
#         if not CustomUser.objects.filter(email=intern, is_intern=True).exists():
#             raise serializers.ValidationError('Intern with this email does not exists')
#         return data

#     def save(self, **kwargs):
#         action = self.validated_data.get('action')
#         intern = self.validated_data.get('intern_id')
#         # intern_email = self.validated_data.get('intern_email')
#         batch = self.context['batch']
#         intern=CustomUser.objects.get(email=intern, is_intern=True)
#         if action == 'approve':
#             batch.approve_intern(intern)
#         elif action == 'reject':
#             batch.reject_intern(intern)
#         elif action == 'request':
#             BatchInternRelation.objects.create(intern=intern, batch=batch, status=BatchInternRelation.PENDING)
#         elif action == 'add':
#             intern_id = CustomUser.objects.get(email=intern)
#             batch.interns.add(intern_id)
#         elif action == 'remove':
#             intern_id = CustomUser.objects.get(email=intern)
#             batch.interns.remove(intern_id)

class BatchRequestSerializer(serializers.Serializer):
    intern_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(is_intern=True))
    action = serializers.ChoiceField(choices=['approve', 'reject', 'request'])

    def validate(self, data):
        intern = data.get('intern_id')
        batch = self.context['batch']
        
        # Ensure the intern has not already been approved/rejected
        if BatchInternRelation.objects.filter(intern=intern, batch=batch).exclude(status=BatchInternRelation.PENDING).exists():
            raise serializers.ValidationError('This intern has already been processed for this batch.')
        
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

# class BatchRequestSerializer(serializers.Serializer):
#     intern_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(is_intern=True))
#     action = serializers.ChoiceField(choices=['add', 'remove'])

#     def validate(self, data):
#         intern = data.get('intern_id')
#         batch = self.context['batch']
        
#         # Ensure the intern has not already been approved/rejected
#         if BatchInternRelation.objects.filter(intern=intern, batch=batch).exclude(status=BatchInternRelation.PENDING).exists():
#             raise serializers.ValidationError('This intern has already been processed for this batch.')
        
#         return data

#     def save(self, **kwargs):
#         action = self.validated_data.get('action')
#         intern = self.validated_data.get('intern_id')
#         batch = self.context['batch']

#         if action == 'approve':
#             batch.approve_intern(intern)
#         elif action == 'reject':
#             batch.reject_intern(intern)
#         elif action == 'request':
#             BatchInternRelation.objects.create(intern=intern, batch=batch, status=BatchInternRelation.PENDING)
#         elif action == 'add':
#             BatchInternRelation.objects.create(intern=intern, batch=batch, status=BatchInternRelation.APPROVED)
#         elif action == 'remove':
#             batch.interns.remove(intern)