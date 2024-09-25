from django.urls import path
from Batches.views import (BatchCreateListView, BatchRetieveView,
                           ApproveRejectInternView, AddRemoveMentorView,
                           InternRequestJoinBatchView)
urlpatterns = [
    path('list_create/', BatchCreateListView.as_view(), name='batch-list-create'),
    path('<int:pk>', BatchRetieveView.as_view(), name='batch-details'),
    path('<int:pk>/join', InternRequestJoinBatchView.as_view(), name='batch-details'),
    path('<int:pk>/approve_reject_intern', ApproveRejectInternView.as_view(), name='batch-add-interns'),
    path('<int:pk>/add_remove_mentor', AddRemoveMentorView.as_view(), name='batch-add-interns'),
]
