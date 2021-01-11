from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist

import datetime
from .models import Patient, Visit, User

# Create your tests here.
class PatientTestCase(TestCase):
  
  def setUp(self):

    # Create Patients
    p1 = Patient.objects.create(
      names='Joaquin Daniel',
      last_names='Negrete Saab',
      bday=datetime.date(2005, 3, 7),
      cel='0999268112',
      id_num='0930336680',
      mail='joaquin.negrete03@gmail.com',
      job='Estudiante',
      fam_histo='Dad has diabetes'
    )
    p2 = Patient.objects.create(
      names='Angie',
      last_names='Saab Saab',
      bday=datetime.date(1969, 5, 25),
      cel='0987211868',
      mail='angie.saab@gmail.com',
      job='Orientadora Familiar'
    )
    p3 = Patient.objects.create(
      names='Joaquin Alberto',
      last_names='Negrete Argenzio',
      bday=datetime.date(1971, 12, 9),
      cel='0998661398',
      id_num='0910301043',
      mail='jnegrete@rocketmail.com',
      job='Ing. Eléctrico'
    )

    # Create Visits
    Visit.objects.create(
      patient=p1,
      date=datetime.datetime(2020, 12, 24, 12, 30, 0, 0),
      symptoms='Left foot ache',
      treatment='Cough syrup'
    )
    Visit.objects.create(
      patient=p1,
      date=datetime.datetime(2020, 12, 25, 12, 30, 0, 0),
      symptoms='Left foot ache',
      treatment='Cough syrup'
    )
    Visit.objects.create(
      patient=p2,
      symptoms='Right arm ache',
      treatment='Paracetamol'
    )

    # Create a sample User
    User.objects.create_user('user', 'user@example.com', 'password')


  # Test model functions
  def test_get_all_visits(self):
    """"Checks if the function to get all the Visits from a Patient work"""
    p = Patient.objects.get(job='Estudiante')
    self.assertEqual(p.get_all_visits().count(), 2)

  def test_get_age(self):
    """Checks if the get_age() function works correctly"""
    p = Patient.objects.get(job='Estudiante')
    self.assertEqual(p.get_age(), 15)

  def test_is_first_visit_true(self):
    """Checks if the is first visit function returns true"""
    p = Patient.objects.get(names='Joaquin Alberto')
    self.assertTrue(p.is_first_visit())

  def test_is_first_visit_false(self):
    """Checks if the is first visit function returns false"""
    p = Patient.objects.get(names='Joaquin Daniel')
    self.assertFalse(p.is_first_visit())


  # Client Testing
  def test_invalid_login(self):
    """Checks the that the status code is 200, because it doesn't should redirect"""
    c = Client()
    response = c.post('/accounts/login/', {'username': 'not_a_user', 'password': 'not_a_password'})

    self.assertEqual(response.status_code, 200)

  def test_valid_login(self):
    """Checks if the status code is 302 because it redirects, for it is a valid User"""
    c = Client()
    response = c.post('/accounts/login/', {'username': 'user', 'password': 'password'})

    self.assertEqual(response.status_code, 302)

  def test_logout(self):
    """Checks if logout returns the correct status code, and if it logs out"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})
    response = c.get('/accounts/logout/')

    self.assertEqual(response.status_code, 302)

    # Checks if you can enter index logged out
    response = c.get('')
    self.assertEqual(response.status_code, 302)

  def test_index(self):
    """Checks if the context count is correct"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})
    response = c.get('')
    
    self.assertEqual(response.context['patients'].count(), Patient.objects.count())

  def test_create_patient(self):
    """Checks if you can correctly create a Patient"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})

    response = c.post('/crear/', {
      'names': 'Si',
      'last_names': 'No',
      'bday': '2000-06-09',
      'cel': '0999999999',
      'id_num': '0910203040',
      'mail': 'si@example.com',
      'job': 'Estudiante',
      'company': '',
      'allergies': '',
      'patho_histo': '',
      'fam_histo': ''
    })

    self.assertEqual(response.status_code, 302)
    self.assertEqual(Patient.objects.last().names, 'Si')

  def test_patient_view(self):
    """If request method is POST, it will create a Visit. Else, it will get all visits"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})

    response = c.get('/paciente/1/')

    p = Patient.objects.get(pk=1)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['patient'].id, 1)
    self.assertEqual(p.get_all_visits().count(), 2)

    response = c.post('/paciente/1/', {
      'symptoms': 'His arm hurts',
      'treatment': 'Cough syrup'
    })

    self.assertEqual(response.status_code, 201)
    self.assertEqual(p.get_all_visits().count(), 3)

  def test_search_patient(self):
    """Checks if the search view works correctly"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})

    response = c.get('/busqueda/?q=negrete')

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['patients'][0].id, 3)
    self.assertEqual(response.context['patients'][1].id, 1)
    self.assertEqual(response.context['patients'].count(), 2)


  def test_edit_patient(self):
    """Checks if you can properly edit a Patient"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})

    response = c.get('/editar/1/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context['patient'].id, 1)

    response = c.post('/editar/1/', {
      'names': 'Joaquin Daniel Si',
      'last_names': 'Negrete Saab',
      'bday': '2005-03-07',
      'cel': '0999268112',
      'id_num': '0930336680',
      'mail': 'joaquin.negrete03@gmail.com',
      'job': 'Estudiante',
      'company': '',
      'allergies': '',
      'patho_histo': '',
      'fam_histo': 'Dad has diabetes'
    })

    p = Patient.objects.get(pk=1)

    self.assertEqual(response.status_code, 302)
    self.assertEqual(p.names, 'Joaquin Daniel Si')

  def test_delete_patient(self):
    """Checks if the delete patient function works"""
    c = Client()
    c.post('/accounts/login/', {'username': 'user', 'password': 'password'})

    response = c.delete('/eliminar/1/')

    patient_exists = True
    try:
      Patient.objects.get(pk=1)
    except ObjectDoesNotExist:
      patient_exists = False

    self.assertEqual(response.status_code, 204)
    self.assertFalse(patient_exists)
