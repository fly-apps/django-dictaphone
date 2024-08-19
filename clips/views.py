from django.core import serializers
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views import View
import json
from .models import Clip

class ClipListView(View):
	def get(self, request):
		clips = Clip.objects.all()
		return render(request, 'clips/index.html', {'clips': clips})

class ClipDetailView(View):
	def get(self, request, path):
		clip = Clip.objects.get(name=path)
		if clip.file:
			return HttpResponse(clip.file.read(), content_type=clip.mime)
		else:
			return HttpResponse(status=404)

	def put(self, request, path):
		clip = Clip.objects.get_or_create(name=path)[0]
		clip.mime = request.headers['Content-Type']
		clip.file.save(path, ContentFile(request.body))
		clip.save()
		record = model_to_dict(clip)
		record.__delitem__('file')
		return HttpResponse(json.dumps(record), content_type='application/json')

	def delete(self, request, path):
		clip = Clip.objects.get(name=path)
		clip.file.delete()
		clip.delete()
		return HttpResponse(status=204)
