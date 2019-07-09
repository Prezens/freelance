from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'price')


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'price', 'consumer', 'executor', 'done')


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'price', 'consumer', 'executor', 'done')


class TaskUpdateExecutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('executor', 'done')
