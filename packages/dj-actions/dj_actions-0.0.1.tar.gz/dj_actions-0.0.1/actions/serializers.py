from rest_framework import serializers
from .models import (
    ActionInstance,
    ActionInstanceTask,
    ActionInstanceTaskRun
)

class ActionInstanceTaskRunSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActionInstanceTaskRun
        fields = '__all__'

class ActionInstanceTaskSerializer(serializers.ModelSerializer):
    attempts = ActionInstanceTaskRunSerializer(read_only=True, many=True)

    class Meta:
        model = ActionInstanceTask
        fields = '__all__'


class ActionInstanceSerializer(serializers.ModelSerializer):

    tasks = ActionInstanceTaskSerializer(read_only=True, many=True)

    class Meta:
        model = ActionInstance
        fields = '__all__'