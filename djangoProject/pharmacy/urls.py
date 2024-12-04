from django.urls import path
from .views import GenerateReportView, generate_report
from . import views

urlpatterns = [
    # Prescription and Report Views
    path('prescription/<int:prescription_id>/', GenerateReportView.as_view(), name='generate_report'),
    path('prescriptions/', generate_report, name='generate_report_all'),
    
    # Other Pharmacy Views
    path('pharmacy/', views.Pharmacy.as_view(), name='pharmacy'),
    path('pharmacy/prescriptions/', views.Prescriptions.as_view(), name='prescriptions'),
    path('prescriptions/add/', views.AddPrescriptionView.as_view(), name='add_prescription'),
    path('view-prescriptions/', views.ViewPrescriptionsView.as_view(), name='view_prescriptions'),
    path('prescriptions/submit/', views.submit_prescription, name='submit_prescription'),

    # Medication Management
    path('pharmacy/medications/', views.Medications.as_view(), name='medications'),
    path('add_medication/', views.AddMedicationView.as_view(), name='add_medication'),
    path('view_medications/', views.ViewMedicationsView.as_view(), name='view_medications'),
    path('manage_medications/', views.ManageMedicationsView.as_view(), name='manage_medications'),
    path('medications/edit/<int:id>/', views.edit_medication, name='edit_medication'),
    path('medications/delete/<int:id>/', views.delete_medication, name='delete_medication'),

    # Help and Support
    path('pharmacy/help/', views.Help.as_view(), name='help'),
    path('help/', views.help_page, name='help'),
    path('help/faq/', views.faq_page, name='faq'),
    path('help/contact_support/', views.contact_support_page, name='contact_support'),
    path('send_support_ticket/', views.send_support_ticket, name='send_support_ticket'),
]
