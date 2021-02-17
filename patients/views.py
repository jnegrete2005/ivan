from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView

import json

from time import sleep
from datetime import datetime

from .models import Patient, Visit

# Create your views here.
class IndexView(ListView):
  model = Patient
  template_name = 'patients/index.html'
  context_object_name = 'patients'
  ordering = ['last_names']
  paginate_by = 12


class SearchView(ListView):
  def get_queryset(self):
    return Patient.objects.filter(last_names__startswith=self.request.GET['q']).order_by('last_names')

  template_name = 'patients/index.html'
  context_object_name = 'patients'
  ordering = ['last_names']
  paginate_by = 12


def patient_view(request, pk):
  patient = get_object_or_404(Patient, pk=pk)

  if request.method == 'POST':
    visit = Visit.objects.create(
      patient=patient,
      symptoms=str(request.POST['symptoms']).strip(),
      treatment=str(request.POST['treatment']).strip()
    )
    visit.save()

    visits = patient.get_all_visits()

    response = render(request, 'patients/patient.html', {
      'patient': patient,
      'visits': visits
    })
    
    response.status_code = 201
    return response

  visits = patient.get_all_visits()

  response = render(request, 'patients/patient.html', {
    'patient': patient,
    'visits': visits
  })

  response.status_code = 200
  return response


def create_patient(request):
  if request.method == 'POST':
    p = Patient.objects.create(
      names=str(request.POST['names']).strip(),
      last_names=str(request.POST['last_names']).strip(),
      bday=datetime.strptime(request.POST['bday'], '%Y-%m-%d').date(),
      cel=str(request.POST['cel']).strip(),
      id_num=str(request.POST['id_num']).strip(),
      mail=str(request.POST['mail']).strip(),
      job=str(request.POST['job']).strip(),
      company=str(request.POST['company']).strip(),
      allergies=str(request.POST['allergies']).strip(),
      patho_histo=str(request.POST['patho_histo']).strip(),
      fam_histo=str(request.POST['fam_histo']).strip(),
      insurance=str(request.POST['insurance']).strip()
    )
    p.save()

    return redirect('patient', pk=p.id)

  return render(request, 'patients/create_patient.html')


@user_passes_test(lambda u: u.is_superuser)
def edit_patient(request, pk):
  p = get_object_or_404(Patient, pk=pk)

  if request.method == 'POST':
    p.names = str(request.POST['names']).strip()
    p.last_names = str(request.POST['last_names']).strip()
    p.bday =  datetime.strptime(request.POST['bday'], '%Y-%m-%d').date()
    p.cel = str(request.POST['cel']).strip()
    p.id_num=str(request.POST['id_num']).strip()
    p.mail=str(request.POST['mail']).strip()
    p.job=str(request.POST['job']).strip()
    p.company=str(request.POST['company']).strip()
    p.allergies=str(request.POST['allergies']).strip()
    p.patho_histo=str(request.POST['patho_histo']).strip()
    p.fam_histo=str(request.POST['fam_histo']).strip()
    p.insurance=str(request.POST['insurance']).strip()

    p.save(update_fields=[
      'names', 'last_names', 'bday', 'cel', 'id_num', 'mail', 'job', 'company', 'allergies', 'patho_histo', 'fam_histo', 'insurance'
      ])

    return redirect('patient', pk=pk)

  return render(request, 'patients/edit_patient.html', {'patient': p})


@user_passes_test(lambda u: u.is_superuser)
def delete_patient(request, pk):
  if request.method == 'DELETE':
    get_object_or_404(Patient, pk=pk).delete()
    return JsonResponse({'message': 'user deleted succesfully'}, status=204)

  return HttpResponseBadRequest()


def edit_visit(request, pk):
  visit = get_object_or_404(Visit, pk=pk)
  if request.method == 'GET':
    return render(request, 'patients/edit_consult.html', {
      'visit': visit
    })

  if request.method == 'POST':
    visit.symptoms = str(request.POST['symptoms']).strip()
    visit.treatment = str(request.POST['treatment']).strip()

    visit.save(update_fields=['symptoms', 'treatment'])

    return redirect('patient', pk=visit.patient.id)

# Login and logout views here
def login_view(request):
  if request.method == 'POST':
    # Attempt to sign user in
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    # Check if authentication successful
    if user is not None:
      login(request, user)
      return redirect('index')
    else:
      return render(request, 'patients/login.html', {
        'message': 'Invalid username and/or password.'
      })
  else:
      return render(request, 'patients/login.html')


def logout_view(request):
  logout(request)
  return redirect('index')
