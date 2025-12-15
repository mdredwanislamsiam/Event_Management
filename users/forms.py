from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.models import Group, Permission
import re
from events.forms import StyledFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomSignUpForm(forms.ModelForm): 
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta: 
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        
    def clean_password(self): 
        password = self.cleaned_data.get('password')
        errors = []
        if len(password) < 8 : 
            errors.append("Password must have at least 8 characters!")
        if not re.search(r'[A-Z]', password): 
            errors.append("Password must have at least one uppercase letter")
        if not re.search(r'[a-z]', password): 
            errors.append("Password must have at least one lowercase letter")
        if not re.search(r'[0-9]', password): 
            errors.append("Password must have at least one number")
        if not re.search(r'[!@#$&%^*?]', password): 
            errors.append(
                "Password must have at least one special character Among: !, @, #, $, &, %, ^, *, ?")
        if re.search(r'[(){}:;/]', password): 
            errors.append(
                "Password must have at least one special character Among: (, ), _, =, -, +, {, }, :, ;, /")
        if errors: 
            raise forms.ValidationError(errors)
        
        return password
    
    def clean(self): 
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password: 
            raise forms.ValidationError("Password do not match!")
        
    def clean_email(self): 
        email = self.cleaned_data.get('email')
        email_exist = User.objects.filter(email = email).exists()
        if email_exist: 
            raise forms.ValidationError("This Email is already registered!")
        
        return email
    
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items(): 
            if field.label != None: 
                field.widget.attrs.update({
                    'class': 'shadow-sm focus:bg-yellow-500 mb-4 rounded-lg w-full p-3',
                    'placeholder': f"Enter {field.label}"
                })
            else: 
               field.widget.attrs.update({
                   'class': 'shadow-sm focus:bg-yellow-500 mb-4 rounded-lg w-full p-3',
                   'placeholder': f"Enter Password"
                   
               })
        
        
class CustomSignInForm(AuthenticationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.label != None:
                field.widget.attrs.update({
                    'class': 'shadow-sm focus:bg-yellow-500 mb-4 rounded-lg w-full p-3',
                    'placeholder': f"Enter {field.label}"
                })
            else:
               field.widget.attrs.update({
                   'class': 'shadow-sm focus:bg-yellow-500 mb-4 rounded-lg w-full p-3',
                   'placeholder': f"Enter Password"

               })


class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset = Group.objects.all(), 
        empty_label="Select a role", 
        widget= forms.Select(attrs={
            'class': 'shadow-sm focus:bg-yellow-500 mb-4 rounded-lg w-full p-3'
        })
    )


class CreateGroupForm( forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type").all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'my-2 bg-white p-4 rounded-lg'    
        }),
        required=False,
        label="Assign Permission",
    )
    class Meta:
        model = Group
        fields = ["name", "permissions"]
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "shadow-sm focus: bg-white mb-4 my-2 rounded-lg w-full p-3", 
                'placeholder': 'Enter your name'
            }), 
        }
    

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm): 
    pass

 
class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm): 
    pass


class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm): 
    pass


class EditProfileForm(StyledFormMixin, forms.ModelForm): 
    class Meta: 
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'bio', 'profile_image']
        
