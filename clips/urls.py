from django.urls import path
from .views import ClipListView, ClipDetailView

urlpatterns = [
    path('', ClipListView.as_view(), name='clips'),
    path("<path:path>", ClipDetailView.as_view(), name='clip'),
]