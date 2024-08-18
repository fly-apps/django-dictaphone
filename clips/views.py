from django.core import serializers
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
import json
from .models import Clip
import urllib.parse

def index(request):
    clips = Clip.objects.all()
    return render(request, 'clips/index.html', {'clips': clips})

def clip(request, path):
    name = urllib.parse.unquote(path)

    if request.method == 'PUT':
        clip = Clip.objects.get_or_create(name=name)[0]
        clip.mime = request.headers['Content-Type']
        clip.save()
        return HttpResponse(json.dumps(model_to_dict(clip)), content_type='application/json')
    
    if request.method == 'DELETE':
        try:
            clip = Clip.objects.get(name=name)
            clip.delete()
            return HttpResponse(status=204)
        except Clip.DoesNotExist:
            return HttpResponse(status=404)