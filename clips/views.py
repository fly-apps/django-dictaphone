from django.shortcuts import render
from .models import Clip

def index(request):
    clips = Clip.objects.all()
    return render(request, 'clips/index.html', {'clips': clips})