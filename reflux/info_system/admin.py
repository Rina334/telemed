from django.contrib import admin
from .models import Doctor, Patient, MedicalExamination

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'specialization', 'phone', 'email')
    search_fields = ('last_name', 'first_name', 'specialization', 'phone', 'email')
    list_filter = ('specialization',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'specialization')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'last_name', 
        'first_name', 
        'age_display',
        'reflux_display',
        'operation_display',
        'pyelonephritis_display',
        'doctor'
    )
    search_fields = ('last_name', 'first_name', 'phone', 'email')
    list_filter = (
        'doctor',
        'left_kidney_grade',
        'right_kidney_grade',
        'operation_type',
        'pyelonephritis_history'
    )
    readonly_fields = ('created_at', 'age_display')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'birth_date', 'photo')
        }),
        ('Медицинская информация', {
            'fields': (
                'left_kidney_grade',
                'right_kidney_grade',
                'operation_type',
                'operation_date',
                'operation_notes',
                'pyelonephritis_history',
                'last_pyelonephritis_date'
            )
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email', 'doctor'),
            'classes': ('collapse',)
        }),
        ('Дополнительно', {
            'fields': ('notes', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def age_display(self, obj):
        return f"{obj.age} лет"
    age_display.short_description = 'Возраст'
    
    def reflux_display(self, obj):
        return f"L:{obj.get_left_kidney_grade_display()} R:{obj.get_right_kidney_grade_display()}"
    reflux_display.short_description = 'Рефлюкс'
    
    def operation_display(self, obj):
        if obj.operation_type != 'NONE':
            return obj.get_operation_type_display()
        return "Нет операции"
    operation_display.short_description = 'Операция'
    
    def pyelonephritis_display(self, obj):
        return "Да" if obj.pyelonephritis_history else "Нет"
    pyelonephritis_display.short_description = 'Пиелонефрит'

@admin.register(MedicalExamination)
class MedicalExaminationAdmin(admin.ModelAdmin):
    list_display = (
        'examination_date',
        'patient_info',
        'doctor_info',
        'reflux_display',
        'pyelonephritis_display',
        'creatinine_display'
    )
    search_fields = (
        'patient__last_name',
        'patient__first_name',
        'doctor__last_name',
        'doctor__first_name'
    )
    list_filter = (
        'examination_date',
        'has_pyelonephritis',
        'left_kidney_grade',
        'right_kidney_grade',
        'doctor'
    )
    date_hierarchy = 'examination_date'
    
    def patient_info(self, obj):
        return f"{obj.patient.last_name} {obj.patient.first_name}"
    patient_info.short_description = 'Пациент'
    
    def doctor_info(self, obj):
        return f"{obj.doctor.last_name} {obj.doctor.first_name[0]}." if obj.doctor else "-"
    doctor_info.short_description = 'Врач'
    
    def reflux_display(self, obj):
        return f"L:{obj.get_left_kidney_grade_display()} R:{obj.get_right_kidney_grade_display()}"
    reflux_display.short_description = 'Рефлюкс'
    
    def pyelonephritis_display(self, obj):
        return "Да" if obj.has_pyelonephritis else "Нет"
    pyelonephritis_display.short_description = 'Пиелонефрит'
    
    def creatinine_display(self, obj):
        return f"{obj.creatinine_level} мг/дл" if obj.creatinine_level else "-"
    creatinine_display.short_description = 'Креатинин'