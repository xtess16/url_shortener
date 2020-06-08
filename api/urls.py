from django.urls import path, include

from api.views import LinksList, LinkDetail

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('links', LinksList.as_view(), name='links'),
    path('link/<pk>/', LinkDetail.as_view(), name='link'),
]