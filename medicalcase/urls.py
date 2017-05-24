from django.conf.urls import url
from medicalcase import views as medicalcase_views

urlpatterns = [
    url(r'^post/medical_case/$', medicalcase_views.MedicalCaseCreate.as_view(), name='medical-case'),
    url(r'^medical_cases/$', medicalcase_views.MedicalCaseList.as_view(), name='medical_cases'),
    url(r'^medical_case/(?P<pk>[0-9]+)/detail/$', medicalcase_views.MedicalCaseDetail.as_view(),
        name='medical_case-detail'),
]
