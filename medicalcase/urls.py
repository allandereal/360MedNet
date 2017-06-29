from django.conf.urls import url
from medicalcase import views as medicalcase_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^post/medical_case/$', login_required(medicalcase_views.MedicalCaseCreate.as_view()), name='medical-case'),
    url(r'^medical_cases/$', login_required(medicalcase_views.MedicalCaseList.as_view()), name='medical_cases'),
    url(r'^medical_case/(?P<pk>[0-9]+)/detail/$', login_required(medicalcase_views.MedicalCaseDetail.as_view()),
        name='medical_case-detail'),
    url(r'medical_case/comment/(?P<pk>[0-9]+)/$', medicalcase_views.medical_case_comment_add_view,
        name='medical-case-comment'),

]
