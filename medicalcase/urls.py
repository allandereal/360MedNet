from django.conf.urls import url
from medicalcase import views as medicalcase_views

urlpatterns = [
    url(r'^post/medical_case/$', medicalcase_views.MedicalCaseCreate.as_view(), name='medical-case'),
    url(r'^medical_cases/$', medicalcase_views.MedicalCaseList.as_view(), name='medical_cases'),
]
