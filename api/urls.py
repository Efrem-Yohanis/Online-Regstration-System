from django.urls import path
from . import views

urlpatterns = [
    path('getalluser/', views.getalluser),
    path('registration/', views.registration),
    path('update/<int:user_id>', views.update),
    path('getuser/<int:user_id>', views.getuser),
    path('delete/<int:user_id>', views.delete),
    
]