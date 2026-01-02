from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from users.models import User
from .models import Student
from .serializers import StudentSerializer

# Role-based permission helper
def is_admin(user):
    return user.role == 'ADMIN'

class StudentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Admin: see all students
        # Teacher: see only their batch students
        if is_admin(request.user):
            students = Student.objects.all()
        else:
            # teacher: get batches they teach
            batches = request.user.batch_set.all()
            students = Student.objects.filter(batch__in=batches)

        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not is_admin(request.user):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRetrieveUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            student = Student.objects.get(pk=pk)
            if not is_admin(user) and student.batch.teacher != user:
                return None
            return student
        except Student.DoesNotExist:
            return None

    def get(self, request, pk):
        student = self.get_object(pk, request.user)
        if not student:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = self.get_object(pk, request.user)
        if not student:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
        if not is_admin(request.user):
            return Response({"detail":"Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        student = self.get_object(pk, request.user)
        if not student:
            return Response({"detail":"Not found"}, status=status.HTTP_404_NOT_FOUND)
        if not is_admin(request.user):
            return Response({"detail":"Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
