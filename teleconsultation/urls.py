from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:appointment_id>/', views.start_teleconsultation, name='start_teleconsultation'),
    path('end/<int:consultation_id>/', views.end_teleconsultation, name='end_teleconsultation'),
    path('list/', views.teleconsultation_list, name='teleconsultation_list'),
]
