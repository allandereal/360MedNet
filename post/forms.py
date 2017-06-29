from django import forms
from django.contrib.auth.models import User
from material.base import Layout, Row, Fieldset
from post.models import Post, Comment


class PostForm(forms.ModelForm):
    post_content = forms.CharField(label='Post  or medical case', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ('title', 'post_content')


class CommentForm(forms.ModelForm):
    comment_content = forms.CharField(label='Comment', widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('comment_content',)
