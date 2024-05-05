from django import forms
from django.contrib.auth.forms import UserCreationForm
from slapify_web_app.models import User, Song


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=[('User', 'User'), ('Artist', 'Artist')])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type')

    # This function cleans data to prevent malicious inputs
    def save(self, commit=True):
        user = super(CreateAccountForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'genre', 'song_file']  # 'Artist' field will be set automatically

    def clean_song_file(self):
        song_file = self.cleaned_data.get('song_file')
        if not song_file.name.endswith('.mp3'):
            raise forms.ValidationError('Only MP3 files are allowed.')
        return song_file