from django.urls import path
from .views import StudentListCreateView, StudentRetrieveUpdateDeleteView

urlpatterns = [
    path('students/', StudentListCreateView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentRetrieveUpdateDeleteView.as_view(), name='student-rud'),
]


