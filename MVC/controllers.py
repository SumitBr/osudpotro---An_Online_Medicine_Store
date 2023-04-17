from django.shortcuts import render

from django.shortcuts import get_object_or_404

from .models import Category, Listing, Cart

# Context Processors
def categories(request):
    return {
        'categories': Category.objects.all()
    }


def listing_all(request):
    listings = Listing.objects.all()
    return render(request, 'home.html', {'listings': listings})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    listings = Listing.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'listings': listings})


def listing_detail(request, listing_slug):
    listing = get_object_or_404(Listing, slug=listing_slug, for_sale=True)
    return render(request, 'listing.html', {'listing': listing})


from django.http import JsonResponse

def cart_summary(request):
    cart = Cart(request)
    return render(request, 'summary.html', {'cart': cart})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        listing_id = int(request.POST.get('listingid'))
        listing_qty = int(request.POST.get('listingqty'))
        listing = get_object_or_404(Listing, id=listing_id)
        cart.add(listing=listing, qty=listing_qty)

        cartqty = cart.__len__()
        response = JsonResponse({'qty': cartqty})
        return response

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        listing_id = int(request.POST.get('listingid'))
        cart.delete(listing=listing_id)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        cartsubtotal = cart.get_subtotal_price()
        response = JsonResponse({'qty': cartqty, 'total': carttotal, 'subtotal': cartsubtotal})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        listing_id = int(request.POST.get('listingid'))
        listing_qty = int(request.POST.get('listingqty'))
        cart.update(listing=listing_id, qty=listing_qty)

        cartqty = cart.__len__()
        carttotal = cart.get_total_price()
        cartsubtotal = cart.get_subtotal_price()
        response = JsonResponse({'qty': cartqty, 'total': carttotal, 'subtotal': cartsubtotal})
        return response


# Context Processors
def cart(request):
    return {'cart': Cart(request)}

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
# from django.utils.encoding import force_bytes, force_str
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# from orders.views import user_orders

from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,SetPasswordForm)

from .models import UserBase

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Username', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    first_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))

    class Meta:
        model = UserBase
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,'edit_details.html', {'user_form': user_form})
 

@login_required
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:account_deletion')  # delete_confirmation => account_deletion


def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = True
            user.save()
            return render(request, 'account_activation.html')
    else:
        registerForm = RegistrationForm()
    return render(request, 'register.html', {'form': registerForm})

