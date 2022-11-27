from django import forms
from .models import Post,Comment,Message

class ExploreForm(forms.Form):

    q=forms.CharField(label='',widget=forms.TextInput(attrs={
        "placeholder":"enter tag ..."
    }))



class MessageForm(forms.ModelForm):

    class Meta:
        
        body=forms.CharField(label='',widget=forms.Textarea(attrs={
            "rows":3,
            "placeholder":"add message"
        }))

        image=forms.ImageField(required=False,label='')
        video=forms.FileField(required=False,label='')
        model=Message

        fields=["body","image","video"]







class ThreadForm(forms.Form):

    username=forms.CharField(max_length=200,label="enter username ... ")



class CommentForm(forms.ModelForm):

    image=forms.ImageField(label='',required=False,widget=forms.ClearableFileInput(attrs={
            "multiple":True
    }))

    comment=forms.CharField(label='',widget=forms.Textarea(attrs={
        'rows':3,
        'placeholder':'add comment ...'
    }))
    class Meta:
        model=Comment
        fields=["comment","image"]


class PostForm(forms.ModelForm):

    image=forms.ImageField(label='',required=False,widget=forms.ClearableFileInput(attrs={
        "multiple":True
    }))

    body=forms.CharField(label='',widget=forms.Textarea(attrs={
        'class':'form-control',
        'rows':3,
        'placeholder':'add post'
    }))
    class Meta:
        model=Post
        fields=["body","image"]