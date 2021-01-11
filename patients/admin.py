from django.contrib import admin
from .models import Patient, Visit, User

# Register your models here.
class AdminPatient(admin.ModelAdmin):
  list_display = (
    'id', 'names', 'last_names', 'bday', 'cel', 'mail', 'job', 'company', 'allergies', 'patho_histo', 'fam_histo'
  )

class AdminVisit(admin.ModelAdmin):
  list_display = (
    'id', 'patient', 'date', 'symptoms', 'treatment'
  )


admin.site.register(Patient, AdminPatient)
admin.site.register(Visit, AdminVisit)
admin.site.register(User)
