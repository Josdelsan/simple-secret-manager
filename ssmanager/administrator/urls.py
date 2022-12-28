from django.urls import path
from administrator import views 
 
urlpatterns = [ 
    path('register', views.register_request),
    path('logout', views.logout_request),
    path('login', views.login_request),
    path('create', views.create_service_request),
    path('list', views.list_services_request),
    path('', views.index),
]