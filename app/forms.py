from django import forms
from app.models import *
from django.contrib.auth.forms import UserCreationForm


class RegisterBuyerForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False, 'placeholder': 'Enter username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    address = forms.CharField(label="Address", widget=forms.TextInput(attrs={'placeholder': 'Enter address'}),
                              max_length=100, error_messages={'required': 'This field is required',
                                                              'invalid': 'Address has maximum 100 characters!'
                                                              })

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "address")

    def save(self, commit=True):
        user = super(RegisterBuyerForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class RegisterSellerForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': False, 'placeholder': 'Enter username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

    SELLER_TYPES = (
        ('P', 'Physical person'),
        ('J', 'Juridical person')
    )

    first_name = forms.CharField(label="First name", widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(label="Last name", widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
    telephone = forms.CharField(label="Telephone",
                                widget=forms.TextInput(attrs={'placeholder': 'Enter telephone number'}),
                                max_length=10, error_messages={'required': 'This field is required',
                                                               'invalid': 'Telephone number has maximum 10 digits!'
                                                               }
                                )
    type_of_seller = forms.ChoiceField(choices=SELLER_TYPES, label="Type of seller")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "telephone", "type_of_seller")

    def save(self, commit=True):
        user = super(RegisterSellerForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class AddProductForm(forms.ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'placeholder': 'Enter product name'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder': 'Enter product '
                                                                                                   'description'}),
                                  max_length=300, error_messages={'required': 'This field is required',
                                                                 'invalid': 'Product description has maximum 300 '
                                                                            'characters! '
                                                                 }
                                  )
    price = forms.FloatField(label="Price", widget=forms.TextInput(attrs={'placeholder': 'Enter product price'}))
    stock = forms.IntegerField(label="Stock", widget=forms.TextInput(attrs={'placeholder': 'Enter product stock'}))

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock')
