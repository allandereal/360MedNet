from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from .models import MedicalCase, Comment


class MedicalCaseForm(forms.ModelForm):
    PURPOSE = (('I need help!', 'I need help!'), ('I found this case interesting.', 'I found this case interesting.'),
               ('I need help!', 'I need help!'))

    purpose = forms.CharField(label='Reason for sharing medical case', widget=forms.Select(choices=PURPOSE))

    class Meta:
        model = MedicalCase

        fields = ('title', 'chief_complaint','patient_age', 'patient_gender', 'patient_country_of_origin',
                  'history_of_present_illness', 'medical_history', 'surgical_history', 'social_history',
                  'family_history', 'allergies', 'medications', 'review_of_systems', 'physical_examination',
                  'diagnostic_tests', 'medical_case_category', 'any_other_details', 'purpose')


class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(label='Comment', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('comment_content',)