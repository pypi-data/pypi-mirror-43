from django.shortcuts import render
from django.conf import settings

def docs_index(request):
    context = {
        "actions": settings.ACTION_MAP
    }
    return render(request, 'actions/index.html', context)
