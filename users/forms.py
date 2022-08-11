from dataclasses import fields
from django.contrib.auth.password_validation import validate_password
from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "예) kream@kream.co.kr",
                "autoComplete": "on",
            },  # off하면 자동완성 해제
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호"})
    )

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:
    #         raise forms.ValidationError("가입하지 않은 유저입니다.")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("비밀번호가 틀립니다."))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("가입하지 않은 유저입니다."))


class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("email", "first_name", "last_name", "phone_number")

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 입력해주세요"})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "비밀번호를 한번 더 입력해주세요"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(username=email)
            raise forms.ValidationError("이미 가입된 이메일입니다.")
        except models.User.DoesNotExist:
            return email

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        validate_password(password)
        if password != password1:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        else:
            return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        try:
            models.User.objects.get(phone_number=phone_number)  # get을 filter로 바꿔도 됨
            raise forms.ValidationError("이미 가입된 전화번호입니다.")
        except models.User.DoesNotExist:
            return phone_number

    def save(self, *args, **kwargs):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()
