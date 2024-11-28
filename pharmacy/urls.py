from . import views
from django.urls import path

urlpatterns = [
    path('pharmacy/', views.Pharmacy.as_view(), name='pharmacy'),
    path('pharmacy/prescriptions/', views.Prescriptions.as_view(), name='prescriptions'),
    path('prescriptions/add/', views.AddPrescriptionView.as_view(), name='add_prescription'),
    path('view-prescriptions/', views.ViewPrescriptionsView.as_view(), name='view_prescriptions'),
    path('prescriptions/submit/', views.submit_prescription, name='submit_prescription'),
    path('pharmacy/medications/', views.Medications.as_view(), name='medications'),
    path('add_medication/', views.AddMedicationView.as_view(), name='add_medication'),
    path('view_medications/', views.ViewMedicationsView.as_view(), name='view_medications'),
    path('manage_medications/', views.ManageMedicationsView.as_view(), name='manage_medications'),
    path('medications/view/', views.ViewMedicationsView.as_view(), name='view_medications'),
    path('medications/edit/<int:id>/', views.edit_medication, name='edit_medication'),
    path('medications/delete/<int:id>/', views.delete_medication, name='delete_medication'),
    path('pharmacy/help/', views.Help.as_view(), name='help'),
    path('summary_report/<int:report_id>/', views.summary_report_view, name='summary_report'),
    path('summary_report/<int:report_id>/pdf/', views.export_pdf, name='export_pdf'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('help/', views.help_page, name='help'),
    path('help/faq/', views.faq_page, name='faq'),
    path('help/contact_support/', views.contact_support_page, name='contact_support'),
    path('send_support_ticket/', views.send_support_ticket, name='send_support_ticket'),
]