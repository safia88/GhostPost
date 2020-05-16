from django import forms
from ghost.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['is_boast', 'content']
