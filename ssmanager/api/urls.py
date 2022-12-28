from django.urls import path
from api import views 
 
urlpatterns = [ 
    path('secrets/list', views.secrets_list),
]