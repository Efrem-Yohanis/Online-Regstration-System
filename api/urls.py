from django.urls import path
from . import views

urlpatterns = [
    path('getalluser/', views.getalluser),
    path('registration/', views.registration),
    path('update/<int:user_id>/', views.update),
    path('patch_req/<int:user_id>/', views.patch_req),
    path('getuser/<int:user_id>/', views.get_user),
    path('delete/<int:user_id>/', views.delete),
    path('options_req/<int:user_id>/', views.options_req),
    
    
    
]