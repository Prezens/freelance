from django.shortcuts import get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from .serializers import *
from .permissions import IsConsumerUser, IsOwnerTask


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskCreateSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerTask)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save(consumer=request.user)

            return Response(status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer


class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()
    lookup_field = 'id'
    serializer_class = TaskDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsConsumerUser)

    @api_view(['POST', 'GET'])
    def accept(request, id):
        task = get_object_or_404(Task, id=id)

        with transaction.atomic():
            request.user.update_balance(task.price, task=task)

        Task.objects.filter(id=id, executor=None).update(executor=request.user, done=True)
        
        return Response({'message': 'Accept'}, status=status.HTTP_200_OK)
