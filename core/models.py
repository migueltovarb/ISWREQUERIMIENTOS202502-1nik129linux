from django.db import models
from django.contrib.auth.models import User

# 1. Specialty (Example: Cardiology, Pediatrics)
class Specialty(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 2. Doctor (Linked to a User Login)
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

# 3. Patient (Linked to a User Login)
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# 4. Appointment (The Cita)
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Appt: {self.patient} with {self.doctor}"
    class Appointment(models.Model):
        STATUS_CHOICES = [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # --- NEW FIELDS ---
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appt: {self.patient} with {self.doctor}"