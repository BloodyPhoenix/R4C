from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import RobotSerializer
from .models import Robot


class CreateRobotAPI(ModelViewSet):
    serializer_class = RobotSerializer
    queryset = Robot.objects.all()

    def create(self, request, *args, **kwargs):
        data = {
            'model': request.data.get('model'),
            'version': request.data.get('version'),
            'created': request.data.get('created')
        }
        data['serial'] = data['model']+'-'+data['version']
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
