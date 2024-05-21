from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('v1/', include('apps.academic.urls')),
    path('v1/', include('apps.ct_requests.urls')),
    path('v1/', include('apps.graphics.urls')),
    path('v1/', include('apps.home.urls')),
    path('v1/', include('apps.register.urls')),
]
