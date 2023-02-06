from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('qa', views.qa, name='qa'),
    path('del/<int:q_id>', views.delete_q, name='delete_q'),
]