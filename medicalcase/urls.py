from django.conf.urls import url
from medicalcase import views as medicalcase_views

urlpatterns = [
    url(r'^medical_case/$', medicalcase_views.MedicalCaseCreate.as_view(), name='Medical Case'),
    url(r'^feed/$', medicalcase_views.medical_case_list, name='feed'),
]
