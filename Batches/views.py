from django.shortcuts import get_object_or_404
from django.db import models

from Batches.models import Batches
from Batches.api.serializers import (BatchRequestSerializer, BatchSerializer)

from accounts.models import CustomUser

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

# Create a new batch or list all batches
class BatchCreateListView(generics.ListCreateAPIView):
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Batches.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
# Approve or Reject an intern request
class ApproveRejectInternView(generics.UpdateAPIView):
    serializer_class = BatchRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Batches, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        batch = self.get_object()

        # Only the batch creator or mentors can approve/reject interns
        if request.user != batch.created_by and not batch.mentors.filter(id=request.user.id).exists():
            return Response({"detail": "You do not have permission to approve/reject interns."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data, context={'batch': batch})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        action = request.data.get('action')
        if action == 'approve':
            return Response({"detail": "Intern request approved."}, status=status.HTTP_200_OK)
        elif action == 'reject':
            return Response({"detail": "Intern request rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


# View for interns to request to join a batch
class InternRequestJoinBatchView(generics.UpdateAPIView):
    serializer_class = BatchRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Batches, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        batch = self.get_object()

        # Only interns can request to join a batch
        if not request.user.is_intern:
            return Response({"detail": "Only interns can request to join batches."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'intern_id': request.user.id, 'action': 'request'}, context={'batch': batch})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Your request to join the batch has been submitted."}, status=status.HTTP_200_OK)

# Add or remove mentors from a batch
class AddRemoveMentorView(generics.RetrieveUpdateAPIView):
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Batches, pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        batch = self.get_object()

        # Only the batch creator can add/remove mentors
        if request.user != batch.created_by:
            return Response({"detail": "Only the batch creator can add or remove mentors."}, status=status.HTTP_403_FORBIDDEN)

        mentor_email = request.data.get('mentor_email')
        mentor = get_object_or_404(CustomUser, email=mentor_email, is_mentor=True)

        action = request.data.get('action')
        if action == 'add':
            batch.mentors.add(mentor)
            return Response({"detail": f"Mentor {mentor.email} added to the batch."}, status=status.HTTP_200_OK)
        elif action == 'remove':
            batch.mentors.remove(mentor)
            return Response({"detail": f"Mentor {mentor.email} removed from the batch."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

class BatchRetieveView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BatchSerializer
    def get_queryset(self):
        # Get the logged-in user
        user = self.request.user
        queryset = Batches.objects.filter(created_by=user)

        # Get query parameters
        status = self.request.query_params.get('status', None)  # e.g., /api/batches?status=true
        role = self.request.query_params.get('role', None)  # e.g., /api/batches?role=mentor

        # Filter by status if provided (e.g., active/inactive batches)
        if status is not None:
            queryset = queryset.filter(status=status.lower() == 'true')

        # Filter by user's role in the batch
        if role:
            if role == 'owner':
                queryset = queryset.filter(created_by=user)
            elif role == 'mentor':
                queryset = queryset.filter(mentors=user)
            elif role == 'intern':
                queryset = queryset.filter(interns=user)
            else:
                queryset = queryset.filter(
                    models.Q(created_by=user) |
                    models.Q(mentors=user) |
                    models.Q(interns=user)
                )

        return queryset.distinct()