from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from .models import MedicalCase, Comment


class MedicalCaseForm(forms.ModelForm):
    patient_gender = forms.CharField(widget=forms.TextInput)
    purpose = forms.CharField(widget=forms.TextInput, label='Reason for sharing medical case')

    class Meta:
        model = MedicalCase

        fields = ('title', 'purpose', 'chief_complaint','patient_age', 'patient_gender', 'patient_country_of_origin',
                  'history_of_present_illness', 'medical_history', 'surgical_history', 'social_history',
                  'family_history', 'allergies', 'medications', 'review_of_systems', 'physical_examination',
                  'diagnostic_tests', 'medical_case_category')


class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(label='Comment', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('comment_content',)