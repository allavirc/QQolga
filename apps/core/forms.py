from django import forms
from apps.core.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'phone', 'category', 'images', 'price']
