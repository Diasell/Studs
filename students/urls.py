from django.conf.urls import url
from rest_framework.authtoken import views as av


urlpatterns = [
    url(r'^api-token-auth/', av.obtain_auth_token),
]