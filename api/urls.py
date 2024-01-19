from django.urls import path
from .views import CustomAuthToken
from . import views

urlpatterns = [
    path('getalluser/', views.getalluser),
    path('api-token-auth/', CustomAuthToken.as_view()),
   
]