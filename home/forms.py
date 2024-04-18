from django import forms
from .models import Post , Comment
class PostUpdateForm(forms.ModelForm):
    class Meta :
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':8})
        }

class CommentCreateForm(forms.ModelForm):
    class Meta :
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':4})
        }
        labels = {
            'body': 'Comment ',
        }

class CommentReplyForm(forms.ModelForm):
    class Meta :
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control','rows':2})
        }
        labels = {
            'body': 'Reply ',
        }


class PostSearchForm(forms.Form):
    search = forms.CharField()