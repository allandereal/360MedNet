from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from post.models import Post


class PostForm(forms.ModelForm):
    post_content = forms.Textarea()

    class Meta:
        model = Post
        fields = ('post_content',)
