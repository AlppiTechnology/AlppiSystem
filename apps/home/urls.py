from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    # path('user/login/', loginviewsets.UserLogin.as_view(), name='login'),

]

urlpatterns = format_suffix_patterns(urlpatterns)