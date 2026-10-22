from django import forms    

class SignIn(forms.Form):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

    email = forms.EmailField(
        widget=forms.EmailInput()
    )

    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(attrs={ 'x-bind:type': "visible ? 'text' : 'password'" })
    )

    remember_me = forms.BooleanField(
        required=False,
        label='Keep me signed in',
        widget=forms.CheckboxInput()
    )