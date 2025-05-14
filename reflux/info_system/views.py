from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Doctor, Patient, MedicalExamination
from .forms import DoctorForm, PatientForm, MedicalExaminationForm

def dashboard(request):
    patients = Patient.objects.select_related('doctor')
    examinations = MedicalExamination.objects.select_related('patient', 'doctor')
    doctors = Doctor.objects.all()

    context = {
        'patients': patients,
        'examinations': examinations,
        'doctors': doctors,
        'Patient': Patient,

    }
    return render(request, 'info_system/dashboard.html', context)

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Доктор успешно добавлен')
        else:
            messages.error(request, 'Ошибка при добавлении доктора')
    return redirect('dashboard')

def add_patient(request):
    if request.method == 'POST':
        print(request)
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пациент успешно добавлен')
        else:
            messages.error(request, 'Ошибка при добавлении пациента')
    return redirect('dashboard')

def add_examination(request):
    if request.method == 'POST':
        form = MedicalExaminationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные осмотра успешно добавлены')
        else:
            messages.error(request, 'Ошибка при добавлении осмотра')
    return redirect('dashboard')

@login_required
def patient_detail(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    examinations = MedicalExamination.objects.filter(patient=patient).order_by('-examination_date')
    
    context = {
        'patient': patient,
        'examinations': examinations,
    }
    return render(request, 'info_system/patient_detail.html', context)