# API URL Patterns

from django.urls import path

urlpatterns = [
    path('api/endpoint1/', Endpoint1View.as_view(), name='endpoint1'),
    path('api/endpoint2/', Endpoint2View.as_view(), name='endpoint2'),
    # Add additional API endpoints here
]