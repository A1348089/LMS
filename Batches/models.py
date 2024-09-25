from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Batches(models.Model):
    batch_name = models.CharField(max_length=100, null=False, default="New_batch")
    created_by = models.ForeignKey(CustomUser, related_name='created_batches', on_delete=models.CASCADE)
    mentors = models.ManyToManyField(CustomUser, related_name="mentor_batches", limit_choices_to={'is_mentor': True})
    
    # Use the through model for interns
    interns = models.ManyToManyField(CustomUser, through='BatchInternRelation', related_name='intern_batches')
    
    # Track the batch status (active/inactive)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.batch_name} - {'Active' if self.status else 'Inactive'}"
    
    def approve_intern(self, intern):
        """Approve an intern's request to join the batch."""
        relation = BatchInternRelation.objects.filter(batch=self, intern=intern, status=BatchInternRelation.PENDING).first()
        if relation:
            relation.status = BatchInternRelation.APPROVED
            relation.save()

    def reject_intern(self, intern):
        """Reject an intern's request to join the batch."""
        relation = BatchInternRelation.objects.filter(batch=self, intern=intern, status=BatchInternRelation.PENDING).first()
        if relation:
            relation.status = BatchInternRelation.REJECTED
            relation.save()

class BatchInternRelation(models.Model):
    PENDING = "P"
    APPROVED = "A"
    REJECTED = "R"

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    )
    # Relationship status between intern and batch
    intern = models.ForeignKey(CustomUser, related_name='batch_relations', on_delete=models.CASCADE, limit_choices_to={'is_intern': True})
    batch = models.ForeignKey(Batches, related_name='intern_relations', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.intern.username} - {self.batch.batch_name} ({self.get_status_display()})"