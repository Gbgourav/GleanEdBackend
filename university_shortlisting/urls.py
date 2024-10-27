from django.urls import path
from .views import UniversityShortlistView

urlpatterns = [
    path('university-shortlist/', UniversityShortlistView.as_view(), name='university-shortlist'),
]
