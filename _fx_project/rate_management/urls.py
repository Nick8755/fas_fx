from django.urls import path
from django.http import JsonResponse
from .views import RateListCreateView

def api_root(request):
    return JsonResponse({
        "message": "Welcome to the FX Rate Management API"
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('rates/', RateListCreateView.as_view(), name='rate-list-create'),
]