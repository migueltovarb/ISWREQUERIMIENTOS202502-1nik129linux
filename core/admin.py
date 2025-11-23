from django.contrib import admin
from .models import Specialty, Doctor, Patient, Appointment

admin.site.register(Specialty)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)