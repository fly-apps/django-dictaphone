from django.core import serializers
from django.core.files.base import ContentFile
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

    if request.method == 'GET':
        try:
            clip = Clip.objects.get(name=name)
            if clip.file:
                return HttpResponse(clip.file.read(), content_type=clip.mime)
            else:
                return HttpResponse(status=404)
        except Clip.DoesNotExist:
            return HttpResponse(status=404)

    if request.method == 'PUT':
        clip = Clip.objects.get_or_create(name=name)[0]
        clip.mime = request.headers['Content-Type']
        clip.file.save(name, ContentFile(request.body))
        clip.save()
        record = model_to_dict(clip)
        record.__delitem__('file')
        return HttpResponse(json.dumps(record), content_type='application/json')
    
    if request.method == 'DELETE':
        try:
            clip = Clip.objects.get(name=name)
            clip.file.delete()
            clip.delete()
            return HttpResponse(status=204)
        except Clip.DoesNotExist:
            return HttpResponse(status=404)