from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import InvalidSpendException, Reimbursement
from django.contrib import messages

def get_all_ads_data():
    reimbursement = Reimbursement()
    all_ads_data = reimbursement.get_ads()
    ad_info = Reimbursement.ad_info

    types = list(ad_info.keys())

    context = {
        'all_ads_data': all_ads_data,
        'ad_info': ad_info,
        'types': types,
    }
    return context

@login_required
def home(request):
    if request.method == 'POST':
        ad_type = request.POST.get('ad_type')
        count = request.POST.get('count')
        spend = request.POST.get('spend')

        if count and count.isdigit():
            count = int(count)
        else:
            count = 0
        try:
            spend = float(spend)
        except ValueError:
            spend = 0.0

        try:
            reimbursement = Reimbursement()
            reimbursement.add_ad(ad_type, count, spend)
        except InvalidSpendException as e:
            messages.error(request, str(e))
            return redirect('home')

        context = get_all_ads_data()
        return render(request, 'reimbursement_app/home.html', context)

    else:
        context = get_all_ads_data()
        return render(request, 'reimbursement_app/home.html', context)


@login_required
def delete_ad(request, ad_id):
    try:
        reimbursement = Reimbursement()
        reimbursement.remove_ad(ad_id)
    except InvalidSpendException as e:
        messages.error(request, str(e))
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'reimbursement_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'reimbursement_app/signup.html', {'form': form})
