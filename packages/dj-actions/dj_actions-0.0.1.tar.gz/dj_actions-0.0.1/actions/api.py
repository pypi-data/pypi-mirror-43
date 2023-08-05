from django.shortcuts import render
from django.http.response import Http404
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, routers, response, exceptions, decorators

from .models import ActionInstance
from .serializers import ActionInstanceSerializer

from django.conf import settings

class ActionDocsViewSet(viewsets.ViewSet):
    def list(self, request):
        docs = settings.ACTION_MAP
        return response.Response(docs)

    def retrieve(self, request, pk=None):
        task_information = settings.ACTION_MAP.get(pk)
        return response.Response(task_information)

class ActionInstanceViewSet(viewsets.ModelViewSet):
    queryset = ActionInstance.objects.all()
    serializer_class = ActionInstanceSerializer

    @decorators.detail_route(methods=['get', 'post'])
    def run(self, request, pk=None):
        print(pk)
        instance = self.get_object()
        instance.run()
        return instance



router = routers.DefaultRouter()
router.register(r'docs', ActionDocsViewSet, base_name='docs')
router.register(r'action', ActionInstanceViewSet, base_name='action')
