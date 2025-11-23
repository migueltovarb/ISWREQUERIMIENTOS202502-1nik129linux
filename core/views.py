from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import time

# Import our Forms and Models
from .forms import PatientRegistrationForm, AppointmentForm, ProfileUpdateForm
from .models import Patient, Doctor, Appointment

# ==========================================
#              PUBLIC VIEWS
# ==========================================

def home(request):
    return render(request, 'core/home.html')

def doctor_list(request):
    query = request.GET.get('q') # Get search term from URL
    
    if query:
        # Search by Doctor Name OR Specialty
        doctors = Doctor.objects.filter(
            Q(user__first_name__icontains=query) | 
            Q(user__last_name__icontains=query) |
            Q(specialty__name__icontains=query)
        )
    else:
        doctors = Doctor.objects.all()

    return render(request, 'core/doctor_list.html', {'doctors': doctors, 'query': query})

# ==========================================
#              AUTH VIEWS
# ==========================================

def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Create User
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # 2. Create Patient Profile
            Patient.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )

            messages.success(request, "Account created! You can now log in.")
            return redirect('login')
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard_redirect(request):
    """The Traffic Cop: Sends users to the right dashboard based on role"""
    try:
        _ = request.user.doctor
        return redirect('doctor_dashboard')
    except:
        return redirect('dashboard')

@login_required
def profile_settings(request):
    try:
        patient = request.user.patient
    except:
        return redirect('home') # Doctors don't use this form yet

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            # Update Patient fields
            patient = form.save()
            
            # Update User fields manually
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_settings')
    else:
        # Pre-fill form
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'phone': patient.phone,
            'address': patient.address
        }
        form = ProfileUpdateForm(instance=patient, initial=initial_data)

    return render(request, 'core/profile_settings.html', {'form': form})

# ==========================================
#            PATIENT VIEWS
# ==========================================

@login_required
def patient_dashboard(request):
    try:
        patient = request.user.patient
    except:
        return redirect('home')

    appointments = Appointment.objects.filter(patient=patient).order_by('-date')
    return render(request, 'core/dashboard.html', {'appointments': appointments})

@login_required
def book_appointment(request):
    try:
        patient = request.user.patient
    except:
        return redirect('home')

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            appt.patient = patient
            
            # --- VALIDATION 1: Business Hours ---
            # Weekends (5=Sat, 6=Sun)
            if appt.date.weekday() >= 5:
                messages.error(request, "⚠️ Doctors do not work on weekends.")
                return render(request, 'core/book_appointment.html', {'form': form})

            # Time (8am - 6pm)
            start_hour = time(8, 0)
            end_hour = time(18, 0)
            if not (start_hour <= appt.time <= end_hour):
                messages.error(request, "⚠️ Clinic hours are 8:00 AM to 6:00 PM.")
                return render(request, 'core/book_appointment.html', {'form': form})

            # --- VALIDATION 2: Collision Check ---
            conflict = Appointment.objects.filter(
                doctor=appt.doctor,
                date=appt.date,
                time=appt.time
            ).exclude(status='cancelled').exists()

            if conflict:
                messages.error(request, "⚠️ That doctor is already booked at that time.")
            else:
                appt.status = 'pending'
                appt.save()
                print(f"📧 EMAIL SIMULATION: Confirmation sent to {request.user.email}")
                messages.success(request, "Appointment Booked Successfully!")
                return redirect('dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'core/book_appointment.html', {'form': form})

@login_required
def edit_appointment(request, appointment_id):
    appt = get_object_or_404(Appointment, id=appointment_id)

    # 1. Check Ownership (must be patient's appointment)
    if appt.patient != request.user.patient:
        messages.error(request, "No tienes permiso para editar esta cita.")
        return redirect('dashboard')

    # 2. Check Status (block only completed or cancelled appointments)
    # This allows 'pending' AND 'confirmed' status for editing.
    if appt.status in ['completed', 'cancelled']:
        messages.error(request, f"Esta cita ya fue {appt.status} y no puede ser modificada.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            # Note: Ideally repeat validations here, but skipped for brevity
            form.save()
            messages.success(request, "Appointment modified successfully.")
            return redirect('dashboard')
    else:
        form = AppointmentForm(instance=appt)

    return render(request, 'core/book_appointment.html', {'form': form, 'is_edit': True})

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Security Check
    if not hasattr(request.user, 'patient') or appointment.patient != request.user.patient:
        return redirect('dashboard')

    # Change this line to allow cancelling if confirmed:
    if appointment.status in ['pending', 'confirmed']: # <-- Check this line
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled.")
    else:
        messages.error(request, "Cannot cancel this appointment.")

    return redirect('dashboard')

@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except:
        return redirect('home')

    appointments = Appointment.objects.filter(doctor=doctor).order_by('date', 'time')
    return render(request, 'core/doctor_dashboard.html', {'appointments': appointments})

@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Security: Doctor must own this appointment
    if not hasattr(request.user, 'doctor') or appointment.doctor != request.user.doctor:
        return redirect('home')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        if new_status == 'completed':
            # Save Medical Notes
            appointment.diagnosis = request.POST.get('diagnosis')
            appointment.prescription = request.POST.get('prescription')
            appointment.status = 'completed'
            appointment.save()
            messages.success(request, "Visit completed & notes saved.")
            
        elif new_status in ['confirmed', 'cancelled']:
            appointment.status = new_status
            appointment.save()
            messages.success(request, f"Appointment updated to {new_status}")
    
    return redirect('doctor_dashboard')