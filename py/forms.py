from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from py.models import Users, Clnts
import datetime
from django.utils.timezone import utc
from django.contrib.auth.hashers import make_password


class UserForm(UserCreationForm):
    first_name = forms.CharField(required=True,
                                 widget=forms.TextInput)
    password1 = forms.CharField(required=True,
                                widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(required=True,
                                widget=forms.PasswordInput(render_value=True))
    email = forms.EmailField(required=True ,
                            widget=forms.EmailInput)
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'password1',
            'password2',
            'email',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
               "Passwords Mismatch",
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        #password_encrypted = pbkdf2_sha256.encrypt(self.cleaned_data['password1'], rounds=12000, salt_size=32)
        curdate = datetime.datetime.utcnow().replace(tzinfo=utc)
        #user_1 = Users.create(user.email,user.password1, curdate)
        #client_1 = Clnts(name=user.first_name, user=user_1, ddate_created= curdate)
        #client_1.save()
        #client_1 = Clnts.create(user.first_name,curdate)// fucking shit this is not working for fucks sake
        #client_1.name = user.first_name
        if commit:
            user.set_password(user.password1)
            user.save()
            user_1 = Users.create(user.email, make_password(user.password1), curdate)
            client_1 = Clnts(name=user.first_name, user=user_1, ddate_created=curdate)
            client_1.save()
        return user

