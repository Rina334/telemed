from django import forms
from .models import Doctor, Patient, MedicalExamination

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialization', 'phone', 'email']
        widgets = {
            'specialization': forms.TextInput(attrs={'placeholder': 'Уролог, нефролог и т.д.'}),
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 
            'last_name', 
            'birth_date', 
            'phone', 
            'email', 
            'doctor',
            'left_kidney_grade', 
            'right_kidney_grade',
            'operation_type',
            'operation_date',
            'operation_notes',
            'pyelonephritis_history',
            'last_pyelonephritis_date',
            'photo',
            'notes'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'operation_date': forms.DateInput(attrs={'type': 'date'}),
            'last_pyelonephritis_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'operation_notes': forms.Textarea(attrs={'rows': 3}),
        }

class MedicalExaminationForm(forms.ModelForm):
    class Meta:
        model = MedicalExamination
        fields = [
            'patient',
            'doctor',
            'examination_date',
            'left_kidney_grade',
            'right_kidney_grade',
            'has_pyelonephritis',
            'creatinine_level',
            'urine_analysis',
            'usg_results',
            'treatment',
            'recommendations'
        ]
        widgets = {
            'examination_date': forms.DateInput(attrs={'type': 'date'}),
            'urine_analysis': forms.Textarea(attrs={'rows': 2}),
            'usg_results': forms.Textarea(attrs={'rows': 2}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'recommendations': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['creatinine_level'].widget.attrs.update({'step': '0.01', 'min': '0'})