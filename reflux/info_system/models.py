from django.db import models
from django.utils import timezone

class Doctor(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

class Patient(models.Model):
    # Степени рефлюкса
    REFLUX_GRADE_CHOICES = [
        (0, 'Нет рефлюкса'),
        (1, 'I степень'),
        (2, 'II степень'),
        (3, 'III степень'),
        (4, 'IV степень'),
        (5, 'V степень'),
    ]
    
    # Виды операций
    OPERATION_TYPE_CHOICES = [
        ('URETERAL_REIMPLANT', 'Уретероцистоанастомоз'),
        ('DEFLUX_INJECTION', 'Инъекция Дефлюкса'),
        ('OTHER', 'Другое'),
        ('NONE', 'Не выполнялась'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    
    # Показатели рефлюкса
    left_kidney_grade = models.IntegerField(choices=REFLUX_GRADE_CHOICES, default=0)
    right_kidney_grade = models.IntegerField(choices=REFLUX_GRADE_CHOICES, default=0)
    
    # Данные об операции
    operation_type = models.CharField(max_length=50, choices=OPERATION_TYPE_CHOICES, default='NONE')
    operation_date = models.DateField(null=True, blank=True)
    operation_notes = models.TextField(blank=True)
    
    # История пиелонефрита
    pyelonephritis_history = models.BooleanField(default=False)
    last_pyelonephritis_date = models.DateField(null=True, blank=True)
    
    # Фото и дополнительные заметки
    photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    @property
    def age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25)

class MedicalExamination(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    examination_date = models.DateField(default=timezone.now)
    
    # Показатели на момент осмотра
    left_kidney_grade = models.IntegerField(choices=Patient.REFLUX_GRADE_CHOICES)
    right_kidney_grade = models.IntegerField(choices=Patient.REFLUX_GRADE_CHOICES)
    has_pyelonephritis = models.BooleanField(default=False)
    creatinine_level = models.FloatField(null=True, blank=True)
    urine_analysis = models.TextField(blank=True)
    usg_results = models.TextField(blank=True)
    
    treatment = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f'Осмотр {self.patient} от {self.examination_date}'