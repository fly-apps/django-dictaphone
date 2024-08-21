from django.core import serializers
from django.core.files.base import ContentFile
from django.http import FileResponse, HttpResponse
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.views import View
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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
			return FileResponse(clip.file, content_type=clip.mime)
		else:
			return HttpResponse(status=404)

	def put(self, request, path):
		clip = Clip.objects.get_or_create(name=path)[0]
		clip.mime = request.headers['Content-Type']
		clip.file.save(path, ContentFile(request.body))
		clip.save()
		record = model_to_dict(clip)
		record.__delitem__('file')
		self.notify()
		return HttpResponse(json.dumps(record), content_type='application/json')

	def delete(self, request, path):
		clip = Clip.objects.get(name=path)
		clip.file.delete()
		clip.delete()
		self.notify()
		return HttpResponse(status=204)
	
	def notify(self):
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)('notify', {
			'type': 'notify',
			'message': 'New clip available'
		})
