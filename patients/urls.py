from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [
  path('', login_required(views.IndexView.as_view()), name='index'),
  path('busqueda/', login_required(views.SearchView.as_view()), name='search'),
  path('paciente/<int:pk>/', login_required(views.patient_view), name='patient'),
  path('crear/', login_required(views.create_patient), name='create_patient'),
  path('editar/<int:pk>/', login_required(views.edit_patient), name='edit_patient'),
  path('eliminar/<int:pk>/', login_required(views.delete_patient), name='delete_patient'),
  
  path('accounts/login/', views.login_view, name='login'),
  path('accounts/logout/', views.logout_view, name='logout'),

  path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('patients/favicon.ico')))
]
