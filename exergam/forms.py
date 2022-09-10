from django import forms
from .models import ExerciseEntry, Rewards, User, UserManager, Post, Followings, Comment, Location

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('usernm','first_nm','last_nm')

        widgets = {
            'Username': forms.TextInput(attrs={'class': 'form-control'}),
            'First Name': forms.TextInput(attrs={'class': 'form-control'}),
            'Last Name': forms.TextInput(attrs={'class': 'form-control'}),
        }
