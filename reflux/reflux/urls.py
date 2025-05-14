from django.contrib import admin
from django.urls import path
from info_system import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('add_examination/', views.add_examination, name='add_examination'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)